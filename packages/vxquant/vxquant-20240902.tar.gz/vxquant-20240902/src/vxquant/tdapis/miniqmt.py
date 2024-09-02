"""MiniQMT Adapter for VXQuant DataModel"""

import polars as pl
import logging
import time
from pathlib import Path
from typing import Union, Optional, Dict, Any, List, Literal, DefaultDict
from multiprocessing import Lock
from collections import defaultdict

try:
    from xtquant import xtdata
    from xtquant import xtconstant
    from xtquant.xttype import (
        StockAccount,
        XtAsset,
        XtAccountStatus,
        XtPosition,
        XtOrder,
        XtTrade,
        XtOrderError,
        XtCancelError,
        XtOrderResponse,
    )
    from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
except ImportError:
    raise ImportError(
        "Please install vxquant first. Please run 'pip install -U miniqmt' to install it."
    )

from vxsched import VXPublisher
from vxutils import to_datetime, retry, to_datetime, to_timestring, VXFuture
from vxutils.datamodel.adapter import VXDataAdapter
from vxquant.models import (
    VXOrder,
    VXTick,
    VXExecRpt,
    VXPosition,
    VXCashInfo,
    VXMarketPreset,
    to_symbol,
)
from vxquant.base import VXBaseTdApi

xtdata.enable_hello = False

qmt_orderstatus_map = {
    xtconstant.ORDER_UNREPORTED: "PendingNew",
    xtconstant.ORDER_WAIT_REPORTING: "PendingNew",
    xtconstant.ORDER_REPORTED: "New",
    xtconstant.ORDER_REPORTED_CANCEL: "New",
    xtconstant.ORDER_PARTSUCC_CANCEL: "PartiallyFilled",
    xtconstant.ORDER_PART_CANCEL: "Canceled",
    xtconstant.ORDER_CANCELED: "Canceled",
    xtconstant.ORDER_PART_SUCC: "PartiallyFilled",
    xtconstant.ORDER_SUCCEEDED: "Filled",
    xtconstant.ORDER_JUNK: "Rejected",
    xtconstant.ORDER_UNKNOWN: "Unknown",
}

order_sides = [
    xtconstant.STOCK_BUY,
    xtconstant.CREDIT_BUY,
    xtconstant.CREDIT_FIN_BUY,
    xtconstant.CREDIT_BUY_SECU_REPAY,
    xtconstant.CREDIT_FIN_BUY_SPECIAL,
    xtconstant.CREDIT_BUY_SECU_REPAY_SPECIAL,
]

market_price_types = [
    xtconstant.MARKET_SH_CONVERT_5_CANCEL,
    xtconstant.MARKET_SH_CONVERT_5_LIMIT,
    xtconstant.MARKET_PEER_PRICE_FIRST,
    xtconstant.MARKET_MINE_PRICE_FIRST,
    xtconstant.MARKET_PEER_PRICE_FIRST,
    xtconstant.MARKET_MINE_PRICE_FIRST,
    xtconstant.MARKET_SZ_INSTBUSI_RESTCANCEL,
    xtconstant.MARKET_SZ_CONVERT_5_CANCEL,
    xtconstant.MARKET_SZ_FULL_OR_CANCEL,
    84,
    85,
    86,
    87,
    88,
    89,
]


miniqmt_tick_adapter = VXDataAdapter(
    VXTick,
    {
        "tick_id": lambda x: str(
            f"{x['stock_code']}@{x['timetag'] if 'timetag' in x else x['time']}"
        ),
        "symbol": "stock_code",
        "open": "open",
        "high": "high",
        "low": "low",
        "lasttrade": "lastPrice",
        "yclose": "lastClose",
        "ysettle": "lastSettlementPrice",
        "amount": "amount",
        "volume": "volume",
        "ask1_p": lambda x: x["askPrice"][0],
        "ask1_v": lambda x: x["askVol"][0],
        "bid1_p": lambda x: x["bidPrice"][0],
        "bid1_v": lambda x: x["bidVol"][0],
        "ask2_p": lambda x: x["askPrice"][1],
        "ask2_v": lambda x: x["askVol"][1],
        "bid2_p": lambda x: x["bidPrice"][1],
        "bid2_v": lambda x: x["bidVol"][1],
        "ask3_p": lambda x: x["askPrice"][2],
        "ask3_v": lambda x: x["askVol"][2],
        "bid3_p": lambda x: x["bidPrice"][2],
        "bid3_v": lambda x: x["bidVol"][2],
        "ask4_p": lambda x: x["askPrice"][3],
        "ask4_v": lambda x: x["askVol"][3],
        "bid4_p": lambda x: x["bidPrice"][3],
        "bid4_v": lambda x: x["bidVol"][3],
        "ask5_p": lambda x: x["askPrice"][4],
        "ask5_v": lambda x: x["askVol"][4],
        "bid5_p": lambda x: x["bidPrice"][4],
        "bid5_v": lambda x: x["bidVol"][4],
        "created_dt": lambda x: to_datetime(
            x["timetag"] if "timetag" in x else x["time"] / 1000
        ),
    },
)

miniqmt_order_adapter = VXDataAdapter(
    VXOrder,
    {
        "order_id": lambda x: str(x.order_id),
        "account_id": "account_id",
        "symbol": "stock_code",
        "order_side": lambda x: ("Buy" if x.order_type in order_sides else "Sell"),
        "position_effect": lambda x: (
            "Open" if x.order_type in order_sides else "Close"
        ),
        "order_type": lambda x: (
            "Market" if x.price_type in market_price_types else "Limit"
        ),
        "price": "price",
        "volume": "order_volume",
        "filled_volume": "traded_volume",
        "filled_vwap": "traded_price",
        "filled_amount": lambda x: x.traded_volume * x.traded_price,
        "status": lambda x: qmt_orderstatus_map.get(x.order_status, "Unknown"),
        "reject_reason": "status_msg",
        "order_remark": "order_remark",
        "strategy_id": "strategy_name",
        "created_dt": lambda x: to_datetime(x.order_time),
    },
)


miniqmt_execrpt_adapter = VXDataAdapter(
    VXExecRpt,
    {
        "execrpt_id": lambda x: str(x.traded_id),
        "account_id": "account_id",
        "order_id": lambda x: str(x.order_id),
        "symbol": "stock_code",
        "order_side": lambda x: ("Buy" if x.order_type in order_sides else "Sell"),
        "position_effect": lambda x: (
            "Open" if x.order_type in order_sides else "Close"
        ),
        "price": "traded_price",
        "volume": "traded_volume",
        "order_remark": "order_remark",
        "strategy_id": "strategy_name",
        "created_dt": lambda x: to_datetime(x.traded_time),
    },
)


miniqmt_position_adapter = VXDataAdapter(
    VXPosition,
    {
        "account_id": "account_id",
        "symbol": "stock_code",
        "volume_today": lambda x: (
            max(x.volume - x.frozen_volume - x.can_use_volume, 0)
        ),
        "volume_his": lambda x: x.frozen_volume + x.can_use_volume,
        "frozen": "frozen_volume",
        "lasttrade": lambda x: (
            round(x.market_value / x.volume, 4) if x.volume > 0 else 0.0
        ),
        "cost": lambda x: x.volume * (x.avg_price if x.avg_price > 0 else x.open_price),
    },
)

miniqmt_cashinfo_adapter = VXDataAdapter(
    VXCashInfo,
    {
        "account_id": "account_id",
        "balance": lambda x: x.total_asset - x.market_value,
        "order_frozen": lambda x: x.total_asset - x.market_value - x.cash,
        "market_value": "market_value",
    },
)


class VXMiniQMTCallback(XtQuantTraderCallback):  # type: ignore

    def __init__(self, tdapi: "VXMiniQMTTdApi", publisher: VXPublisher) -> None:
        self._tdapi = tdapi
        self._publisher = publisher

    def on_account_status(self, account_status: XtAccountStatus) -> None:
        if account_status.status == xtconstant.ACCOUNT_STATUS_OK:
            logging.debug(f"Account status: {account_status.status}")
        else:
            logging.error(f"Account status error: {account_status.status}")
        self._publisher("on_account_status", data={"account_status": account_status})

    def on_disconnected(self) -> None:
        """掉线通知回调函数"""
        try:
            logging.error("Disconnected from server... waiting for reconnect...")
            self._tdapi.close()
        except Exception as e:
            logging.error(f"Failed to process disconnected event: {e}")

    def on_stock_asset(self, data: XtAsset) -> None:
        logging.info(f"Stock asset: {data}")

    def on_stock_order(self, data: XtOrder) -> None:
        """委托更新回调函数

        Arguments:
            data {XtOrder} -- 交易订单信息
        """
        try:
            order = miniqmt_order_adapter(data)
            logging.debug(f"Receive order status updated: {order}")
            self._publisher(
                "on_order_status",
                data={"order": order},
                channel=self._tdapi.account.account_id,
            )
        except Exception as e:
            logging.error(f"Failed to process order status: {e},data:{data}")

    def on_stock_position(self, data: XtPosition) -> None:
        logging.error(f"Stock position: {data}")

    def on_stock_trade(self, data: XtTrade) -> None:
        """成交回报回调函数

        Arguments:
            data {XtTrade} -- 成交信息
        """
        try:
            execrpt = miniqmt_execrpt_adapter(data)
            logging.debug(f"Receive trade report: {execrpt}")
            self._publisher(
                "on_execution_report",
                data={"execrpt": execrpt},
                channel=self._tdapi.account.account_id,
            )
        except Exception as e:
            logging.error(f"Failed to process trade report: {e},data:{data}")

    def on_order_error(self, data: XtOrderError) -> None:
        """委托错误回调函数

        Arguments:
            data {XtOrderError} -- 报错信息
        """
        try:

            qmt_orders = self._tdapi.trader.query_stock_orders(self._tdapi._account)
            for qmt_order in qmt_orders:
                if qmt_order.order_id == data.order_id:
                    order = miniqmt_order_adapter(qmt_order)
                    order.reject_reason = f"{data.error_id}--{data.error_msg}"
                    order.status = "Rejected"
                    logging.warning(
                        f"Order {data.order_id} error: {order.error_id}--{order.error_msg}"
                    )
                    self._publisher(
                        "on_order_status",
                        data={"order": order},
                        channel=self._tdapi.account.account_id,
                    )
                    break
        except Exception as e:
            logging.error(f"Failed to process order error: {e}")

    def on_cancel_error(self, data: XtCancelError) -> None:
        logging.warning(
            f"Order {data.order_id} Cancel error: {data.error_id}--{data.error_msg}"
        )

    def on_order_stock_async_response(self, data: XtOrderResponse) -> None:
        logging.debug(f"Order stock async response: {data}")
        future = self._tdapi.async_results(data.seq)
        if future.set_running_or_notify_cancel():
            future.set_result(data)


class VXMiniQMTTdApi(VXBaseTdApi):

    def __init__(
        self,
        path: Union[str, Path],
        account_id: str,
        account_type: str = "STOCK",
    ) -> None:
        self._xt_trader: Optional[XtQuantTrader] = None
        self._path = path
        self._account = StockAccount(
            account_id=account_id, account_type=account_type.upper()
        )
        self._publisher = VXPublisher()
        self._async_results: DefaultDict[int, VXFuture] = defaultdict(VXFuture)
        self._lock = Lock()

    @property
    def account(self) -> StockAccount:
        return self._account

    def async_results(self, seq: int) -> VXFuture:
        return self._async_results[seq]

    def register_callback(self, publisher: VXPublisher) -> None:
        self._publisher = publisher

    @property
    @retry(
        3,
        cache_exceptions=(RuntimeError, ConnectionError, TimeoutError),  # type: ignore
        delay=0.3,
        backoff=2,
    )
    def trader(self) -> XtQuantTrader:
        with self._lock:
            if self._xt_trader:
                return self._xt_trader

            self._xt_trader = XtQuantTrader(
                self._path,
                int(time.time()),
                callback=VXMiniQMTCallback(self, self._publisher),
            )

            # 不要阻塞下单通道
            self._xt_trader.set_relaxed_response_order_enabled(True)
            self._xt_trader.start()
            connect_result = self._xt_trader.connect()
            if connect_result != 0:
                raise ConnectionError(
                    f"Failed to start XtQuantTrader, connect error_code: {connect_result}"
                )
            logging.info("XtQuantTrader started successfully...")

            subscribe_result = self._xt_trader.subscribe(self._account)
            if subscribe_result != 0:
                raise RuntimeError(
                    f"Failed to subscribe account, subscribe error_code: {subscribe_result}"
                )
            logging.info(
                f"Account[{self._account.account_id}] subscribed successfully..."
            )
            return self._xt_trader

    def close(self) -> None:
        with self._lock:
            try:
                if self._xt_trader:
                    self._xt_trader.stop()
            except Exception as e:
                logging.error(f"Failed to stop XtQuantTrader: {e}")
            finally:
                self._xt_trader = None

    def current(self, *symbols: str) -> pl.DataFrame:
        ticks = xtdata.get_full_tick(symbols)
        if not ticks:
            return pl.DataFrame(
                {col: [value] for col, value in VXTick().model_dump().items()}
            ).clear()
        datas = {}
        for stock_code, tick in ticks.items():
            tick["stock_code"] = stock_code
            datas[stock_code] = miniqmt_tick_adapter(tick)
        return pl.DataFrame([tick.model_dump() for tick in datas.values()])

    def get_positions(self, symbol: Optional[str] = None) -> pl.DataFrame:

        positions = self.trader.query_stock_positions(self._account)
        if not positions:
            return pl.DataFrame(
                {
                    col: [value]
                    for col, value in VXPosition(
                        account_id=self._account.account_id, symbol="000001.SH"
                    )
                    .model_dump()
                    .items()
                }
            ).clear()

        if symbol:
            return pl.DataFrame(
                [
                    miniqmt_position_adapter(pos).model_dump()
                    for pos in positions
                    if pos.symbol == symbol and pos.volume > 0
                ]
            )
        else:
            return pl.DataFrame(
                [
                    miniqmt_position_adapter(pos).model_dump()
                    for pos in positions
                    if pos.volume > 0
                ]
            )

    def get_orders(
        self, order_id: Optional[str] = None, is_open: bool = True
    ) -> pl.DataFrame:

        orders = self.trader.query_stock_orders(self._account, cancelable_only=is_open)
        if not orders:
            return pl.DataFrame(
                {col: [value] for col, value in VXOrder().model_dump().items()}
            ).clear()

        return (
            pl.DataFrame(miniqmt_order_adapter(order).model_dump() for order in orders)
            if order_id is None
            else pl.DataFrame(
                miniqmt_order_adapter(order).model_dump()
                for order in orders
                if order.order_id == order_id
            )
        )

    def get_execrpts(self, execrpt_id: Optional[str] = None) -> pl.DataFrame:
        """获取成交"""

        execrpts = self.trader.query_stock_trades(self._account)
        if not execrpts:
            return pl.DataFrame(
                {col: [value] for col, value in VXExecRpt().model_dump().items()}
            ).clear()
        if execrpt_id:
            return pl.DataFrame(
                [
                    miniqmt_execrpt_adapter(execrpt)
                    for execrpt in execrpts
                    if execrpt.traded_id == execrpt_id
                ]
            )
        else:
            return pl.DataFrame(
                miniqmt_execrpt_adapter(execrpt) for execrpt in execrpts
            )

    def get_cash(self) -> VXCashInfo:
        cash = self.trader.query_stock_asset(self._account)
        return miniqmt_cashinfo_adapter(cash)  # type: ignore

    def _order_batch(self, *orders: VXOrder) -> Dict[int, VXOrder]:

        placed_orders = {}
        for order in orders:

            seq = self.trader.order_stock_async(
                self._account,
                order.symbol,
                order_type=(
                    xtconstant.STOCK_BUY
                    if order.order_side == "Buy"
                    else xtconstant.STOCK_SELL
                ),
                order_volume=order.volume,
                price_type=(
                    xtconstant.FIX_PRICE
                    if order.order_type == "Limit"
                    else xtconstant.MARKET_PEER_PRICE_FIRST
                ),
                price=order.price,
                strategy_name=order.strategy_id,
                order_remark=order.order_remark,
            )
            if seq < 0:
                order.status = "Rejected"
                order.reject_reason = f"Failed to place order: {seq}"
                continue
            placed_orders[seq] = order
            logging.debug(f"Order placed: {seq} with {order}")
        return placed_orders

    def order_batch(self, *orders: VXOrder) -> List[VXOrder]:
        placed_orders = self._order_batch(*orders)
        for seq, order in placed_orders.items():
            resq = self._async_results[seq].result()
            order.order_id = str(resq.order_id)
        return list(placed_orders.values())

    def _make_order(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = None,
        order_remark: str = "",
        strategy_id: str = "",
    ) -> VXOrder:
        """生成委托订单

        Arguments:
            symbol {str} -- 证券代码
            volume {int} -- 下单数量，正数为买，负数为卖
            price {Optional[float]} -- 委托价格 (default: {None})
            order_remark {str} -- 下单备注 (default: {""})
            strategy_id {str} -- 策略ID (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        symbol = to_symbol(symbol)
        order_side = "Buy" if volume > 0 else "Sell"
        order_type = (
            "Market"
            if price is None
            and VXMarketPreset(symbol=symbol).security_type != "BOND_CONVERTIBLE"  # type: ignore
            else "Limit"
        )
        if price is None:
            ticks = xtdata.get_full_tick([symbol])
            price = (
                ticks[symbol]["askPrice"][0]
                if order_side == "Buy"
                else ticks[symbol]["bidPrice"][0]
            )

        return VXOrder(
            account_id=self._account.account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_side=order_side,
            order_type=order_type,
            position_effect="Open" if volume > 0 else "Close",
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = None,
        order_remark: str = "",
        strategy_id: str = "",
    ) -> VXOrder:
        """下单函数

        Arguments:
            symbol {str} -- 证券代码
            volume {int} -- 下单数量，正数为买，负数为卖
            price {Optional[float]} -- 委托价格 (default: {None})
            order_remark {str} -- 下单备注 (default: {""})
            strategy_id {str} -- 策略ID (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        order = self._make_order(
            symbol=symbol,
            volume=volume,
            price=price,
            order_remark=order_remark,
            strategy_id=strategy_id,
        )
        return self.order_batch(order)[0]

    def order_cancel(self, *orders: Union[str, VXOrder]) -> List[str]:
        """撤单函数

        Arguments:
            order_id {str} -- 委托订单号
        """
        ret_orders = []
        for order in orders:
            order_id = int(order.order_id if isinstance(order, VXOrder) else order)
            cancel_result = self.trader.cancel_order_stock_async(
                self._account, order_id
            )
            if cancel_result <= 0:
                logging.error(f"Failed to cancel order: {order_id}")
                # raise RuntimeError(f"Failed to cancel order: {order_id}")
            ret_orders.append(str(order_id))

        return ret_orders

    def auto_repo(
        self,
        reversed_balance: float = 0.0,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> Optional[VXOrder]:
        """自动回购函数

        Arguments:
            reversed_balance {float} -- 回购金额
            symbols {List[str]} -- 证券代码列表

        Keyword Arguments:
            strategy_id {str} -- 策略ID (default: {""})
            order_remark {str} -- 下单备注 (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        cash = self.get_cash()
        if cash.available < reversed_balance:  # type: ignore
            raise ValueError("Available cash is not enough for repo...")

        target_repo_balance = cash.available - reversed_balance  # type: ignore
        target_repo_volume = int(target_repo_balance // 100 // 10 * 10)
        if target_repo_volume <= 0:
            return None

        if not symbols:
            symbols = ["131810.SZ", "204001.SH"]

        ticks = xtdata.get_full_tick(symbols)

        target_repo_symbol = ""
        target_price = 0.0
        for stock_code, tick in ticks.items():
            if tick["bidPrice"][0] > 0:
                target_repo_symbol = stock_code
                target_price = tick["bidPrice"][0]
        if target_repo_symbol == "" or target_price <= 0.0:
            return None

        logging.info(
            f"Auto repo: {target_repo_symbol} {target_repo_volume} price:{target_price}"
        )
        return self.order_volume(
            symbol=symbols[0],
            volume=-target_repo_volume,
            price=target_price,
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

    def auto_ipo_bond_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        """自动新债申购函数

        Arguments:
            symbols {List[str]} -- 申购证券代码列表，若为空则根据策略自动选择，否则按照列表顺序申购
            strategy_id {str} -- 策略ID
            order_remark {str} -- 交易备注

        Returns:
            List[VXOrder] -- _description_
        """

        ipos = self.trader.query_ipo_data()
        orders = []
        for symbol, info in ipos.items():
            if info["type"] != "BOND":
                continue

            if symbols is None or symbol in symbols:
                order = self.order_volume(
                    symbol=symbol,
                    volume=info["maxPurchaseNum"],
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO BOND: {symbol} {info}")
        return orders

    def auto_ipo_stock_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        orders = []

        ipo_limits = self.trader.query_ipo_data(self._account)
        ipos = self.trader.query_ipo_data()

        for symbol, info in ipos.items():
            if info["type"] != "STOCK":
                continue

            if symbols is None or symbol in symbols:
                if symbol.startswith("0"):
                    ipo_limit = ipo_limits["SZ"]
                elif symbol.startswith("787"):
                    ipo_limit = ipo_limits["SH"]
                else:
                    ipo_limit = ipo_limits["KCB"]

                order = self.order_volume(
                    symbol=symbol,
                    volume=min(info["maxPurchaseNum"], ipo_limit),
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO STOCK: {symbol} {info}")
        return orders

    def order_rebalance(
        self,
        target_weights: Dict[str, float],
        delta: float = 10000.00,
        position_ratio: float = 1.0,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        """动态调仓函数

        Arguments:
            target_portfolios {Dict[str,float]} -- 目标持仓比例

        Keyword Arguments:
            delta {float} -- 单票偏离容忍度 (default: {10000.00})
            position_ratio {float} -- 持仓比例 (default: {1.0})

        Returns:
            List[VXOrder] -- 下单订单列表
        """
        sell_orders: List[VXOrder] = []
        buy_orders: List[VXOrder] = []
        ret_orders: List[VXOrder] = []

        cash = self.get_cash()
        target_value = cash.nav * position_ratio  # type: ignore
        logging.debug(f"Rebalance target value: {target_value}")
        src_positions = self.get_positions()
        dst_positions = pl.DataFrame(
            [
                {"symbol": symbol, "weight": weight}
                for symbol, weight in target_weights.items()
            ],
            schema={"symbol": pl.Utf8, "weight": pl.Float64},
        ).with_columns(
            weights=pl.col("weight") / pl.col("weight").sum(),
        )
        unfinished_orders = self.get_orders(is_open=True)
        unfinished_orders_symbols = unfinished_orders["symbol"].to_list()

        # 1 去掉清仓股票
        closeout_positions = src_positions.filter(
            [
                pl.col("available") > 0,
                pl.col("symbol").is_in(dst_positions["symbol"]).not_(),
            ]
        )
        if not closeout_positions.is_empty():
            for row in closeout_positions.rows(named=True):
                if row["symbol"] in unfinished_orders_symbols:
                    logging.warning(f"Order {row['symbol']} is still in progress...")
                    continue

                order = self._make_order(
                    symbol=row["symbol"],
                    volume=-row["available"],
                    price=row["lasttrade"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                sell_orders.append(order)

        # 2 计算调仓股票

        diff_positions = (
            dst_positions.join(src_positions, on="symbol", how="left")
            .with_columns(
                target_value=pl.col("weight") * target_value,
                diff=pl.col("weight") * target_value - pl.col("market_value"),
            )
            .filter(pl.col("diff").abs() > delta)
            .sort("diff")
        )
        if not diff_positions.is_empty():

            for row in diff_positions.filter(pl.col("diff") < 0).rows(named=True):
                if row["symbol"] in unfinished_orders_symbols:
                    logging.warning(f"Order {row['symbol']} is still in progress...")
                    continue

                # 计算卖出数量
                adjust_volume = max(
                    row["diff"]
                    / row["lasttrade"]
                    // VXMarketPreset(row["symbol"]).volume_unit  # type: ignore
                    * VXMarketPreset(row["symbol"]).volume_unit,  # type: ignore
                    -row["available"],
                )
                if adjust_volume == 0:
                    continue
                order = self._make_order(
                    symbol=row["symbol"],
                    volume=int(adjust_volume),
                    price=row["lasttrade"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                sell_orders.append(order)

            ret_orders = self.order_batch(*sell_orders)
            cash = self.get_cash()
            available_cash = cash.available

            for row in diff_positions.filter(pl.col("diff") > 0).rows(named=True):
                if row["symbol"] in unfinished_orders_symbols:
                    logging.warning(f"Order {row['symbol']} is still in progress...")
                    continue

                # 计算买入数量
                adjust_value = min(available_cash, row["diff"])
                adjust_volume = (
                    adjust_value
                    // row["lasttrade"]
                    // VXMarketPreset(row["symbol"]).volume_unit  # type: ignore
                    * VXMarketPreset(row["symbol"]).volume_unit  # type: ignore
                )
                if adjust_volume <= 0:
                    continue
                order = self._make_order(
                    symbol=row["symbol"],
                    volume=int(adjust_volume),
                    price=row["lasttrade"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                if adjust_volume > 0:
                    available_cash = max(
                        0, available_cash - order.volume * order.price * 1.001  # type: ignore
                    )
                buy_orders.append(order)

        # 3 计算建仓股票
        new_positions = dst_positions.filter(
            pl.col("symbol").is_in(src_positions["symbol"]).not_()
        ).with_columns(
            target_value=pl.col("weight") * target_value,
        )
        if not new_positions.is_empty():
            ticks = self.trader.get_full_tick(new_positions["symbol"].to_list())
            cash = self.get_cash()
            available_cash = cash.available
            for row in new_positions.rows(named=True):
                if row["symbol"] in unfinished_orders_symbols:
                    logging.warning(f"Order {row['symbol']} is still in progress...")
                    continue

                adjust_value = min(available_cash, row["target_value"])
                adjust_volume = (
                    adjust_value
                    // ticks[row["symbol"]]["askPrice"][0]
                    // VXMarketPreset(row["symbol"]).volume_unit  # type: ignore
                    * VXMarketPreset(row["symbol"]).volume_unit  # type: ignore
                )
                if adjust_volume <= 0:
                    continue

                order = self._make_order(
                    symbol=row["symbol"],
                    volume=int(row["target_value"] // row["lasttrade"]),
                    price=ticks[row["symbol"]]["askPrice"][0],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                if adjust_volume > 0:
                    available_cash = max(
                        0, available_cash - order.volume * order.price * 1.001  # type: ignore
                    )  # type: ignore
                buy_orders.append(order)
        ret_orders += self.order_batch(*buy_orders)
        return ret_orders


if __name__ == "__main__":
    import re
    from vxutils import loggerConfig, timer

    loggerConfig()
    tdapi = VXMiniQMTTdApi("*********", account_id="*********")

    logging.info(tdapi.get_cash())
    # logging.info("==== positions ====")
    # logging.info(tdapi.get_positions())
    logging.info("==== orderss ====")
    logging.info(tdapi.get_orders(is_open=False))
    logging.info("==== execrpts ====")
    logging.info(tdapi.get_execrpts())
    # order = tdapi.order_volume(
    #    "600869.SH", 100, price=3.50, strategy_id="test", order_remark="async"
    # )
    # print(order)
    # tdapi.order_cancel(order)

    # tdapi.order_cancel("1745879041")
    # order = tdapi.auto_repo(strategy_id="repo", order_remark="auto repo")
    # logging.info(order)
    with timer("order_rebalance", warnning=0.001):
        orders = tdapi.order_rebalance({"300896.SZ": 0.5, "300059.SZ": 0.5})
        tdapi.order_cancel(*orders)

    df = pl.DataFrame([order.model_dump() for order in orders])
    logging.info(df)
    df.write_csv("orders.csv")
