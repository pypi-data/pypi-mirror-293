from .exchange import Exchange
from quantguard.model.balance import Balance
from quantguard.model.position import Position
from quantguard.model.order import Order, DimensionEnum
from quantguard.model.ledger import Ledger, LedgerType
import time
import logging
from ccxt import gate
import datetime

logger = logging.getLogger(__name__)


# TODO 只实现了合约的定义，spot和合约应该单独提供类
class GATE(Exchange):
    def __init__(self, account_name: str, config: dict):
        super().__init__("gate", account_name, config)
        self.exchange: gate = self.exchange

    def fetch_balance(self) -> Balance:
        ccxt_balance = super().fetch_balance(({"type": "swap"}))
        # print(f"account {self.account_name} balance: {ccxt_balance}")
        created_at = int(time.time() * 1000)
        balance = Balance(
            name=self.account_name,
            exchange=self.exchange_id,
            asset="USDT",
            total=ccxt_balance["USDT"]["total"],  # 总资产 ，不包含了pnl
            available=ccxt_balance["USDT"]["free"],
            frozen=ccxt_balance["USDT"]["used"],
            borrowed=0,  # TODO
            ts=int(ccxt_balance["info"][0]["update_time"]) * 1000,
            unrealized_pnl=ccxt_balance["info"][0]["unrealised_pnl"],
            created_at=created_at,
        )
        return balance

    def fetch_positions(self) -> list[Position]:
        ccxt_position = super()._fetch_positions()
        # print(f"account {self.account_name} position: {ccxt_position}")
        positions = []
        created_at = int(time.time() * 1000)
        for pos in ccxt_position:
            # "DOGE/USDT:USDT"
            base_asset = pos["symbol"].split("/")[0]
            quote_asset = pos["symbol"].split("/")[1].split(":")[0]
            position = Position(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type="UFUTURES",
                base_asset=base_asset,
                quote_asset=quote_asset,
                ts=pos["timestamp"] if pos["timestamp"] else 0,
                # dimension=pos["side"] if pos["side"] else "",
                dimension=DimensionEnum.QUANTITY.value,
                quantity=float(pos["info"]["size"]) * float(pos["contractSize"]),
                average_price=pos["entryPrice"],
                unrealized_pnl=pos["unrealizedPnl"],
                liquidation_price=pos["liquidationPrice"],
                contract_size=pos["contractSize"],
                created_at=created_at,
            )
            positions.append(position)
        return positions

    def fetch_orders_T(self, fetch_orders_T=1):
        since = super().get_yesterday_timestamps(fetch_orders_T)
        open_orders = self.loop_fetch_open_orders(since=since)
        closed_orders = self.loop_fetch_closed_orders(since=since)
        all_orders = open_orders + closed_orders
        my_trades = self.loop_fetch_my_trades(since=since)
        map_my_trades = {}
        for trade in my_trades:
            # order_id 可能有多条
            order_id = trade["info"]["order_id"]
            fee = float(trade["info"]["fee"])
            # 使用 setdefault 初始化或累加
            map_my_trades[order_id] = map_my_trades.setdefault(order_id, 0) + fee

        orders = []
        for order in all_orders:
            # 'symbol': 'DOGE/USDT:USDT'
            base_asset = order["symbol"].split("/")[0]
            quote_asset = order["symbol"].split("/")[1].split(":")[0]

            market_type = "UFUTURES"
            contract_size = self.fetch_symbol_contract_size(order["symbol"])

            # 自定义id去除t-开头 t-1629782400000
            cId = order["clientOrderId"]
            if cId.startswith("t-"):
                cId = cId[2:]

            my_trade_fee = map_my_trades.get(order["id"])
            if my_trade_fee is None:
                logger.warning(f"gate order_id: {order['id']} not found in my_trades")
                result = self.exchange.privateFuturesGetSettleMyTrades(
                    {"settle": "usdt", "type": "swap", "order": order["id"]}
                )
                for tmp in result:
                    my_trade_fee += float(tmp["info"]["fee"])

            item = Order(
                name=self.account_name,
                exchange=self.exchange_id,
                market_type=market_type,
                base_asset=base_asset,
                quote_asset=quote_asset,
                market_order_id=order["id"],
                custom_order_id=cId,
                ts=order["timestamp"],
                origin_price=order["price"],
                origin_quantity=float(order["amount"]) * contract_size,  # 委托数量 > 0
                total_average_price=(
                    order["average"] if order["average"] else 0
                ),  # 总成交均价
                total_filled_quantity=float(order["filled"])
                * contract_size,  # 成交数量 > 0
                # last_average_price=order["info"]["fill_price"],  # 最新成交价格
                # last_filled_quantity=float(order["info"]["size"]) * contract_size,  # 最新成交数量, sell为-1
                order_side=order["side"],
                order_time_in_force=order["timeInForce"],
                reduce_only=order["info"]["is_reduce_only"],
                order_type=order["type"],
                order_state=order["status"],
                dimension=DimensionEnum.QUANTITY.value,
                commission=my_trade_fee if my_trade_fee else 0,
                contract_size=contract_size,
                created_at=int(time.time() * 1000),
            )
            orders.append(item)
        return orders

    def loop_fetch_open_orders(self, since=None, offset=0):
        all_open_orders = []

        while True:
            open_orders = self.exchange.fetch_open_orders(
                since=since, params={"type": "swap"}
            )

            if len(open_orders) == 0:
                break

            last_time = open_orders[-1]["timestamp"]
            logger.info(
                f"length: {len(open_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
            )

            all_open_orders.extend(open_orders)

            if last_time < since:
                break

            offset += len(open_orders)

        return all_open_orders

    def loop_fetch_closed_orders(self, since=None, offset=0):
        all_closed_orders = []

        while True:
            closed_orders = self.exchange.fetch_closed_orders(
                since=since, params={"type": "swap", "offset": offset}
            )

            if len(closed_orders) == 0:
                break

            last_time = closed_orders[-1]["timestamp"]
            logger.info(
                f"length: {len(closed_orders)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
            )

            all_closed_orders.extend(closed_orders)

            if last_time < since:
                break

            offset += len(closed_orders)

            # 为避免触发API限速，可以添加适当的延迟
            time.sleep(0.4)  # 假设当前接口限制：5次/2秒

        return all_closed_orders

    def loop_fetch_my_trades(self, since=None, offset=0):
        all_trades = []

        while True:
            # 获取当前批次的交易数据
            my_trades = self.exchange.fetch_my_trades(
                since=since, params={"type": "swap", "offset": offset}
            )

            if len(my_trades) == 0:
                break

            # 追加当前批次的交易数据到 all_trades 列表中
            all_trades.extend(my_trades)

            last_time = my_trades[-1]["timestamp"]
            logger.info(
                f"length: {len(my_trades)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
            )

            # 如果获取到的最后一笔交易的时间戳小于 since，终止循环
            if last_time < since:
                break

            # 更新 offset 以获取下一批数据
            offset += len(my_trades)
            time.sleep(0.4)

        return all_trades

    def fetch_ledgers_T(self, fetch_orders_T=1):
        since = int(super().get_yesterday_timestamps(fetch_orders_T))
        offset = 0
        ledgers = []
        
        my_trades = self.loop_fetch_my_trades(since=since)
        map_my_trades = {}
        for trade in my_trades:
            map_my_trades[trade["info"]["trade_id"]] = trade["info"]["order_id"]

        while True:
            ccxt_ledgers = self.exchange.fetch_ledger(
                params={"type": "swap", "offset": offset}
            )

            if len(ccxt_ledgers) == 0:
                break

            for ledger in ccxt_ledgers:
                item = self.build_ledger(ledger, map_my_trades.get(ledger["info"]["trade_id"]))
                if not item:
                    continue
                ledgers.append(item)

            last_time = ccxt_ledgers[-1]["timestamp"]
            logger.info(
                f"length: {len(ccxt_ledgers)}, fee length: {len(ledgers)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(since/1000))}"
            )

            # 如果获取到的最后一个账单的时间戳小于 since，终止循环
            if last_time < since:
                break
            # 更新offset以获取下一批数据
            offset += len(ccxt_ledgers)
        return ledgers + self.fetch_ledgers_30(map_my_trades) + self.fetch_ledgers_07_31(map_my_trades)

    def fetch_ledgers_30(self, map_my_trades: dict):
        from_time = int(
            time.mktime(datetime.datetime(2024, 7, 1, 0, 0, 0).timetuple()) * 1000
        )
        to_time = int(
            time.mktime(datetime.datetime(2024, 7, 29, 0, 0, 0).timetuple()) * 1000
        )
        offset = 0
        ledgers = []
        while True:
            params = {"type": "swap", "offset": offset}
            params["from"] = int(from_time / 1000)
            params["to"] = int(to_time / 1000)
            ccxt_ledgers = self.exchange.fetch_ledger(params=params)

            if len(ccxt_ledgers) == 0:
                break

            for ledger in ccxt_ledgers:
                item = self.build_ledger(ledger, map_my_trades.get(ledger["info"]["trade_id"]))
                if not item:
                    continue
                ledgers.append(item)

            last_time = ccxt_ledgers[-1]["timestamp"]
            logger.info(
                f"length: {len(ccxt_ledgers)}, fee length: {len(ledgers)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(from_time/1000))}"
            )

            # 如果获取到的最后一个账单的时间戳小于 since，终止循环
            if last_time < from_time:
                break
            # 更新offset以获取下一批数据
            offset += len(ccxt_ledgers)
        return ledgers
    
    def fetch_ledgers_07_31(self, map_my_trades: dict):
        from_time = int(
            time.mktime(datetime.datetime(2024, 7, 29, 0, 0, 0).timetuple()) * 1000
        )
        to_time = int(
            time.mktime(datetime.datetime(2024, 8, 15, 0, 0, 0).timetuple()) * 1000
        )
        offset = 0
        ledgers = []
        while True:
            params = {"type": "swap", "offset": offset}
            params["from"] = int(from_time / 1000)
            params["to"] = int(to_time / 1000)
            ccxt_ledgers = self.exchange.fetch_ledger(params=params)

            if len(ccxt_ledgers) == 0:
                break

            for ledger in ccxt_ledgers:
                item = self.build_ledger(ledger, map_my_trades.get(ledger["info"]["trade_id"]))
                if not item:
                    continue
                ledgers.append(item)

            last_time = ccxt_ledgers[-1]["timestamp"]
            logger.info(
                f"length: {len(ccxt_ledgers)}, fee length: {len(ledgers)}, data_time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_time/1000))}, since {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(from_time/1000))}"
            )

            # 如果获取到的最后一个账单的时间戳小于 since，终止循环
            if last_time < from_time:
                break
            # 更新offset以获取下一批数据
            offset += len(ccxt_ledgers)
        return ledgers

    def build_ledger(self, ledger, order_id):
        contract = ledger["info"].get("contract", "")
        if not contract or "_" not in contract:
            asset = ""
            symbol = ""
        else:
            asset = contract.split("_")[1]
            symbol = contract.replace("_", "-")
        item = Ledger(
            name=self.account_name,
            exchange=self.exchange_id,
            asset=asset,
            symbol=symbol,
            ts=ledger["timestamp"],
            market_type="UFUTURES",
            # market_id="%s_%s" % (time.time_ns(), ledger["info"]["trade_id"]),
            market_id="%s_%s_%s_%s" % (ledger["timestamp"], ledger["info"]["balance"], ledger["info"]["trade_id"], symbol),
            trade_id=ledger["info"]["trade_id"],
            order_id=order_id if order_id else "",
            ledger_type="",
            amount=float(ledger["info"]["change"]),
            created_at=int(time.time() * 1000),
        )
        if ledger["type"] == "trade" and ledger["info"]["type"] == "pnl":
            item.ledger_type = LedgerType.TRADE_PNL.value
            return item
        if ledger["type"] == "fee" and ledger["info"]["type"] == "fund":
            item.ledger_type = LedgerType.FUNDING_FEE.value
            return item
        if ledger["type"] == "fee" and ledger["info"]["type"] == "fee":
            item.ledger_type = LedgerType.COMMISSION_FEE.value
            return item
        return None
