"""交易/行情接口基础类"""

import logging
from datetime import datetime
from typing import Any, Optional, Dict, List, Optional, Dict, List, Union

import polars as pl
from tqdm import tqdm
from vxsched import VXPublisher
from vxutils import to_datetime, Datetime, import_by_config
from vxquant.models import (
    VXOrder,
    VXCashInfo,
    VXCalendar,
    VXInstruments,
    VXMarketPreset,
)


class VXDataProvider:
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    def update_data(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError


class VXStorageMixin:
    __storage__: Dict[str, Any]

    def save(self, data: pl.DataFrame, identify: str) -> Any:
        """保存到本地

        Arguments:
            data {pl.DataFrame} -- 带保存的数据
            identify {str} -- 标识符
        """
        raise NotImplementedError

    def read(self, identify: str) -> Any:
        """读取数据

        Arguments:
            identify {str} -- 标识符

        Returns:
            Any -- _description_
        """
        raise NotImplementedError

    def clear(self, identify: str) -> None:
        """清除数据

        Arguments:
            identify {str} -- 标识符

        """
        raise NotImplementedError


class VXCalendarProvider(VXDataProvider, VXStorageMixin):

    def __call__(self) -> VXCalendar:
        cal = VXCalendar()
        try:

            trade_dates = self.read("calendar").filter(pl.col("is_trade_day") == 1)[
                "trade_date"
            ]
            cal.update_data(trade_dates=trade_dates)
        except BaseException as err:
            logging.error(f"Failed to load calendar data: {err}", exc_info=True)
        return cal

    def update_data(self, data: pl.DataFrame) -> None:
        cal = self.__call__()
        cal.update_data(
            trade_dates=data.filter(pl.col("is_trade_day") == 1)["trade_date"]
        )
        self.save(cal.data, "calendar")


class VXInstrumentsProvider(VXDataProvider, VXStorageMixin):
    def __call__(
        self,
        name: str,
    ) -> VXInstruments:

        try:
            registrations = self.read(name)
            return VXInstruments(name=name, registrations=registrations)
        except BaseException as err:
            logging.error(f"Failed to load instruments data: {err}", exc_info=True)
            return VXInstruments(name=name)

    def update_data(self, name: str, data: pl.DataFrame) -> None:
        instruments = VXInstruments(name=name, registrations=data)
        instruments.rebuild()
        self.save(data=instruments.registrations, identify=name)


class VXHistoryProvider(VXDataProvider, VXStorageMixin):
    __identity__ = ""

    def __call__(
        self,
        symbols: List[str],
        start_date: Optional[Datetime] = None,
        end_date: Optional[Datetime] = None,
    ) -> pl.DataFrame:

        start_dt: datetime = (
            to_datetime(start_date) if start_date is not None else datetime(1990, 1, 1)
        )

        end_dt: datetime = (
            to_datetime(end_date) if end_date is not None else datetime.now()
        )
        unique_symbols = list(set(symbols))
        if len(unique_symbols) > 200:
            unique_symbols = tqdm(unique_symbols, desc="Loading history data")  # type: ignore
        datas = []
        for symbol in unique_symbols:
            data = self.read(symbol)
            if not data.is_empty():
                datas.append(data)
        df = (
            (
                pl.concat(datas)
                .filter(
                    pl.col("trade_date") >= start_dt, pl.col("trade_date") <= end_dt
                )
                .sort(["symbol", "trade_date"])
            )
            if datas
            else pl.DataFrame({})
        )
        return df  # type: ignore

    def update_data(
        self,
        data: pl.DataFrame,
    ) -> None:
        pbar = tqdm(data["symbol"].unique())
        for symbol in pbar:
            new_data = data.filter(pl.col("symbol") == symbol)
            if new_data.is_empty():
                continue
            pbar.set_description(f"Updating {symbol} {new_data.shape[0]} records")
            old_data = self.__call__([symbol])
            if old_data.is_empty():
                df = new_data
                self.save(data=df, identify=symbol)
            else:
                df = (
                    pl.concat([old_data, new_data])
                    .sort("trade_date")
                    .with_columns(
                        [
                            pl.when(
                                pl.col("trade_date") == pl.col("trade_date").shift(-1)
                            )
                            .then(pl.lit(True))
                            .otherwise(pl.lit(False))
                            .alias("is_duplicate")
                        ]
                    )
                    .filter(pl.col("is_duplicate").not_())
                    .select(pl.exclude("is_duplicate"))
                    .drop_nulls()
                )
                if not df.is_empty():
                    self.save(data=df, identify=symbol)


class VXDayHistoryProvider(VXHistoryProvider):
    __identity__ = "day"


class VXMinHistoryProvider(VXHistoryProvider):
    __identity__ = "min"


class VXFactorProvider(VXDataProvider, VXStorageMixin):
    def __call__(
        self,
        symbols: List[str],
        factor_name: str,
        start_date: Optional[pl.Datetime] = None,
        end_date: Optional[pl.Datetime] = None,
    ) -> Any:

        start_dt = (
            to_datetime(start_date) if start_date is not None else datetime(1990, 1, 1)
        )
        end_dt = to_datetime(end_date) if end_date is not None else datetime.now()
        data = self.read(factor_name)
        if data.is_empty():
            return pl.DataFrame({})
        return data.filter(
            pl.col("symbol").is_in(symbols),
            pl.col("trade_date") >= start_dt,
            pl.col("trade_date") <= end_dt,
        )

    def update_data(self, data: pl.DataFrame, factor_name: str) -> None:
        """更新因子数据

        Arguments:
            data {pl.DataFrame} -- 因子数据
            factor_name {str} -- 因子名称
        """
        if len(set(data.columns) - set(["symbol", "trade_date", factor_name])) != 0:
            raise ValueError(
                f"Data must have columns: symbol, trade_date, and {factor_name}, but got {set(data.columns)}",
            )

        old_data = self.read(factor_name)
        if old_data.is_empty():

            self.save(data.drop_nulls(), factor_name)
        else:
            df = (
                pl.concat([old_data, data])
                .sort(["trade_date", "symbol"])
                .with_columns(
                    [
                        pl.when(
                            (pl.col("trade_date") == pl.col("trade_date").shift(-1))
                            & (pl.col("symbol") == pl.col("symbol").shift(-1))
                        )
                        .then(pl.lit(True))
                        .otherwise(pl.lit(False))
                        .alias("is_duplicate")
                    ]
                )
                .filter(pl.col("is_duplicate").not_())
                .select(pl.exclude("is_duplicate"))
                .drop_nulls()
            )
            if not df.is_empty():
                print("saving data...")
                self.save(df, factor_name)


class VXMdAPI:
    def __init__(self, **params: Any) -> None:
        if "calendar" in params:
            self._calendar_provider = import_by_config(params["calendar"])
        else:
            self._calendar_provider = VXCalendarProvider()

        if "instruments" in params:
            self._instruments_provider = import_by_config(params["instruments"])
        else:
            self._instruments_provider = VXInstrumentsProvider()

        if "day_history" in params:
            self._day_history_provider = import_by_config(params["day_history"])
        else:
            self._day_history_provider = VXDayHistoryProvider()

        if "min_history" in params:
            self._min_history_provider = import_by_config(params["min_history"])
        else:
            self._min_history_provider = VXMinHistoryProvider()

        if "factor" in params:
            self._factor_provider = import_by_config(params["factor"])
        else:
            self._factor_provider = VXFactorProvider()

    def market_preset(self, symbol: str) -> VXMarketPreset:
        return VXMarketPreset(symbol)

    @property
    def calendar(self) -> VXCalendarProvider:
        return self._calendar_provider  # type: ignore

    @property
    def instruments(self) -> VXInstrumentsProvider:
        return self._instruments_provider  # type: ignore

    @property
    def day_history(self) -> VXDayHistoryProvider:
        return self._day_history_provider  # type: ignore

    @property
    def min_history(self) -> VXMinHistoryProvider:
        return self._min_history_provider  # type: ignore

    @property
    def factor(self) -> VXFactorProvider:
        return self._factor_provider  # type: ignore


class VXBaseTdApi:

    def register_callback(self, publisher: VXPublisher) -> None:
        """注册回调函数

        Arguments:
            publisher {VXPublisher} -- 发布器

        """
        raise NotImplementedError

    def current(self, *symbol: str) -> pl.DataFrame:
        """获取当前行情"""
        raise NotImplementedError

    def get_cash(self) -> VXCashInfo:
        """获取现金"""
        raise NotImplementedError

    def get_positions(self, symbol: Optional[str] = None) -> pl.DataFrame:
        """获取持仓"""
        raise NotImplementedError

    def get_orders(
        self, order_id: Optional[str] = None, is_open: bool = True
    ) -> pl.DataFrame:
        """获取订单"""
        raise NotImplementedError

    def get_execrpts(self, execrpt_id: Optional[str] = None) -> pl.DataFrame:
        """获取成交"""
        raise NotImplementedError

    def order_batch(self, *orders: VXOrder) -> List[VXOrder]:
        """批量下单"""
        raise NotImplementedError

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
        raise NotImplementedError

    def order_cancel(self, *orders: Union[str, VXOrder]) -> List[str]:
        """撤单函数

        Arguments:
            orders {Union[str, VXOrder]} -- 订单ID或者订单信息

        Returns:
            List[str] -- 返回撤单订单信息ID
        """
        raise NotImplementedError

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
        raise NotImplementedError

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
        raise NotImplementedError

    def auto_ipo_stock_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        """自动新股申购函数

        Keyword Arguments:
            symbols {Optional[List[str]]} -- 申购证券代码列表，若为空则根据策略自动选择，否则按照列表顺序申购 (default: {None})
            strategy_id {str} -- 策略ID (default: {""})
            order_remark {str} -- 交易备注 (default: {""})

        Returns:
            List[VXOrder] -- 下单订单信息
        """
        raise NotImplementedError

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
        raise NotImplementedError
