"""抽象基类"""

import polars as pl
import logging
import re
from uuid import uuid4
from functools import lru_cache
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import List, Union, Dict, Optional, Any, Literal, Callable, NamedTuple

from pydantic import Field, PlainValidator, computed_field
from vxutils.datamodel.core import VXDataModel
from vxutils import Datetime, to_datetime, to_json, to_enum
from vxquant.constants import (
    ExecType,
    OrderStatus,
    OrderSide,
    OrderType,
    PositionEffect,
    OrderRejectCode,
    SecType,
    DEFAULT_PRESET,
    T0_ETFLOF,
    CASH_SECURITIES,
    DEFULAT_SYMBOL_MAP,
)

try:
    from typing import Annotated  # type: ignore
except ImportError:
    from typing_extensions import Annotated  # type: ignore


__all__ = [
    "default_formatter",
    "symbol_parser",
    "to_symbol",
    "VXSymbol",
    "VXCalendar",
    "VXInstruments",
    "VXMarketPreset",
    "VXSubPortfolio",
    "VXPortfolio",
    "VXTick",
    "VXBar",
    "VXExecRpt",
    "VXOrder",
    "VXPosition",
    "VXCashInfo",
]


class VXSymbol(NamedTuple):
    exchange: str
    code: str


_CODE_TO_EXCHANGE = {
    "0": "SZSE",
    "1": "SZSE",
    "2": "SZSE",
    "3": "SZSE",
    "4": "BJSE",
    "5": "SHSE",
    "6": "SHSE",
    "7": "SHSE",
    "8": "BJSE",
    "9": "SHSE",
}


def default_formatter(symbol: VXSymbol) -> str:
    return f"{symbol.code}.{symbol.exchange.upper()[:2]}"


def symbol_parser(symbol: str) -> VXSymbol:
    # todo 用正则表达式进行进一步优化
    symbol = symbol.strip().upper()

    match_obj = re.match(r"^(\d{6,10})$", symbol)
    if match_obj:
        code = match_obj[1]
        exchange = _CODE_TO_EXCHANGE.get(code[0], "UNKNOWN")
        return VXSymbol(exchange, code)

    match_obj = re.match(r"^[A-Za-z]{2,4}.?([0-9]{6,10})$", symbol)

    if not match_obj:
        match_obj = re.match(r"^([0-9]{6,10}).?[A-Za-z]{2,4}$", symbol)

    if match_obj is None:
        raise ValueError(f"{symbol} format is not support.")

    code = match_obj[1]
    exchange = symbol.replace("SE", "").replace(".", "").replace(code, "")
    if exchange in {"OF", "ETF", "LOF", ""}:
        exchange = _CODE_TO_EXCHANGE.get(code[0], "UNKNOWN")
    elif exchange in {"XSHG", "XSZG", "XBJG", "XSHE", "XSZE", "XBJE"}:
        exchange = exchange[1:3]
    exchange = exchange if len(exchange) > 2 else f"{exchange}SE"
    return VXSymbol(exchange.upper(), code)


@lru_cache(200)
def to_symbol(
    instrument: str, *, formatter: Callable[[VXSymbol], Any] = default_formatter
) -> Any:
    """格式化symbol

    Arguments:
        instrument {str} -- 需要格式化的symbol

    Keyword Arguments:
        formatter {Callable[[str, str], str]} -- 格式化函数 (default: {default_formatter})

    Returns:
        str -- 格式化后的symbol
    """
    if instrument.upper() in {"CNY", "CACH"}:
        return "CNY"

    symbol = symbol_parser(instrument)
    return formatter(symbol)


class VXCalendar:
    def __init__(
        self,
        trade_dates: Optional[Union[pl.Series, List[date], List[datetime]]] = None,
    ):
        self._data = pl.DataFrame(
            {
                "trade_date": pl.date_range(
                    date(1990, 1, 1), date.today().replace(month=12, day=31), eager=True
                )
            }
        ).with_columns(
            [
                pl.lit(False).cast(pl.Boolean).alias("is_trade_day"),
            ]
        )
        if trade_dates is None:
            return
        elif isinstance(trade_dates, list):
            trade_dates = pl.Series(trade_dates)
        trade_dates = trade_dates.map_elements(
            lambda x: to_datetime(x).date(), return_dtype=pl.Date
        )
        self.update_data(trade_dates)

    @property
    def data(self) -> pl.DataFrame:
        return self._data

    def update_data(
        self, trade_dates: Union[pl.Series, List[Union[datetime, date, str, float]]]
    ) -> None:
        """更新交易日数据"""
        if not isinstance(trade_dates, pl.Series):
            trade_dates = pl.Series(trade_dates)

        trade_dates = trade_dates.map_elements(
            lambda x: to_datetime(x).date(), return_dtype=pl.Date
        )

        if max(trade_dates) > self._data["trade_date"].max():
            self._data = pl.concat(
                [
                    self._data,
                    pl.DataFrame(
                        {
                            "trade_date": pl.date_range(
                                self._data["trade_date"].max() + timedelta(days=1),  # type: ignore
                                max(trade_dates).replace(month=12, day=31),
                                eager=True,
                            ),
                        }
                    ),
                ]
            )

        self._data = self._data.with_columns(
            pl.when(pl.col("trade_date").is_in(trade_dates))
            .then(True)
            .otherwise(pl.col("is_trade_day"))
            .alias("is_trade_day")
        )

    @property
    def max(self) -> date:
        return self._data["trade_date"].max()  # type: ignore

    def add_holidays(
        self,
        start_date: Union[str, date, datetime, float],
        end_date: Union[str, date, datetime, float],
        holidays: List[Union[str, date, datetime, float]],
    ) -> None:
        """添加节假日"""
        formatted_holidays: pl.Series = pl.Series(holidays).map_elements(
            lambda x: to_datetime(x).date(), return_dtype=pl.Date
        )
        if formatted_holidays:
            start_date = max(to_datetime(start_date).date(), formatted_holidays.min())
            end_date = min(to_datetime(end_date).date(), formatted_holidays.max())
        else:
            start_date = to_datetime(start_date).date()
            end_date = to_datetime(end_date).date()
        trade_dates = pl.DataFrame(
            {"trade_date": pl.date_range(start_date, end_date, eager=True)}
        ).with_columns(
            pl.col("trade_date").not_().is_in(formatted_holidays).alias("is_trade_day")
        )[
            "trade_date"
        ]
        self.update_data(trade_dates)

    def is_trade_day(
        self,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> bool:
        """判断是否交易日"""
        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return (
            input_date in self._data.filter(pl.col("is_trade_day") == 1)["trade_date"]
        )

    def next_n_trade_day(
        self,
        n: int = 1,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> date:
        """获取下n个交易日"""
        if n < 1:
            raise ValueError("n should be greater than 0")

        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return self._data.filter(pl.col("trade_date") > input_date)["trade_date"][n - 1]  # type: ignore

    def prev_n_trade_day(
        self,
        n: int = 1,
        input_date: Optional[Union[datetime, date, float, str]] = None,
    ) -> date:
        """获取前n个交易日"""
        if n < 1:
            raise ValueError("n should be greater than 0")

        input_date = (
            to_datetime(input_date).date() if input_date is not None else date.today()
        )
        return self._data.filter(pl.col("trade_date") < input_date)["trade_date"][-n]  # type: ignore

    def date_range(
        self,
        start_date: Union[str, date, datetime, float],
        end_date: Union[str, date, datetime, float],
        perion: Literal["D", "W", "M"] = "D",
    ) -> pl.Series:
        """获取日期范围"""
        start_date = to_datetime(start_date).date()
        end_date = to_datetime(end_date).date()
        return self._data.filter(
            [pl.col("trade_date") >= start_date, pl.col("trade_date") <= end_date]
        )["trade_date"]


class VXInstruments:
    """股票池类"""

    def __init__(self, name: str, registrations: Optional[pl.DataFrame] = None) -> None:
        self._name = name
        self._registrations = (
            registrations.with_columns(
                [
                    pl.col("start_date").map_elements(
                        to_datetime, return_dtype=pl.Datetime
                    ),
                    pl.col("end_date").map_elements(
                        to_datetime, return_dtype=pl.Datetime
                    ),
                ]
            )
            if registrations is not None
            else pl.DataFrame(
                {"symbol": [], "start_date": [], "end_date": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            )
        )
        self._last_updated_dt = (
            datetime.today()
            if self._registrations.height == 0
            else to_datetime(self._registrations["end_date"].max())  # type: ignore
        )

    @property
    def name(self) -> str:
        """股票池名称"""
        return self._name

    def __str__(self) -> str:
        return f"< 证券池({self._name})  最新证券:\n {self.list_instruments()} >"

    @property
    def registrations(self) -> pl.DataFrame:
        """股票池出入注册表

        Returns:
            pl.DataFrame -- 注册表
        """
        return self._registrations

    def list_instruments(self, trade_date: Optional[Datetime] = None) -> List[str]:
        """列出股票池中的证券

        Keyword Arguments:
            trade_date {Datetime} -- 交易日，若为空，则为当前日期 (default: {None})

        Returns:
            List[InstrumentType] -- 股票列表
        """
        trade_date = (
            to_datetime(trade_date) if trade_date is not None else datetime.today()
        )

        inst = self._registrations.filter(
            [(pl.col("start_date") <= trade_date), (pl.col("end_date") >= trade_date)]
        )

        return inst["symbol"].to_list()

    def add_instrument(
        self,
        symbol: str,
        start_date: Datetime,
        end_date: Optional[Datetime] = None,
        #
    ) -> "VXInstruments":
        try:
            symbol = to_symbol(symbol)
            start_date = to_datetime(start_date)
            end_date = to_datetime(end_date) if end_date else start_date
        except Exception as e:
            raise ValueError(f"参数错误: {e}")

        self._registrations.vstack(
            pl.DataFrame(
                [
                    {
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                ],
                schema={
                    "symbol": str,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            ),
            in_place=True,
        )
        return self

    def update_components(
        self,
        instruments: List[str],
        start_date: Datetime,
        end_date: Datetime,
    ) -> "VXInstruments":
        """按增量更新股票池"""

        end_date = to_datetime(end_date)
        start_date = to_datetime(start_date)

        new_instruments = pl.DataFrame(
            [
                {
                    "symbol": to_symbol(symbol),
                    "start_date": start_date,
                    "end_date": end_date,
                }
                for symbol in instruments
            ],
            schema={
                "symbol": pl.Utf8,
                "start_date": pl.Datetime,
                "end_date": pl.Datetime,
            },
        )

        self._registrations = pl.concat([self._registrations, new_instruments])
        self.rebuild()
        return self

    @classmethod
    def load(cls, name: str, instruments_file: Union[str, Path]) -> "VXInstruments":
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if not instruments_file.exists():
            raise FileNotFoundError(f"{instruments_file} 不存在。")
        if instruments_file.suffix in {".csv"}:
            registrations = pl.read_csv(instruments_file)
        elif instruments_file.suffix in {".parquet"}:
            registrations = pl.read_parquet(instruments_file)
        else:
            raise ValueError(f"{instruments_file} 文件格式不支持。")

        return VXInstruments(name, registrations)

    def dump(
        self,
        instruments_file: Union[str, Path],
        *,
        file_suffix: Literal["csv", "parquet"] = "csv",
    ) -> "VXInstruments":
        """保存相关信息"""
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if Path(instruments_file).is_dir():
            instruments_file = Path(instruments_file, f"{self._name}.{file_suffix}")

        if file_suffix == "csv":
            self._registrations.write_csv(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        elif file_suffix == "parquet":
            self._registrations.write_parquet(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        else:
            raise ValueError(f"{file_suffix} 文件格式不支持。")
        return self

    def rebuild(self) -> "VXInstruments":
        """重建登记表"""

        new_registrations = []
        temp_registrations = {}

        for rows in self._registrations.sort(by=["symbol", "start_date"]).iter_rows(
            named=True
        ):
            symbol = rows["symbol"]

            if symbol not in temp_registrations:
                temp_registrations[symbol] = rows
            elif (
                temp_registrations[symbol]["end_date"] + timedelta(days=1)
                >= rows["start_date"]
                and temp_registrations[symbol]["end_date"] < rows["end_date"]
            ):
                temp_registrations[symbol]["end_date"] = rows["end_date"]

            elif (temp_registrations[symbol]["end_date"]) < rows["start_date"]:
                new_registrations.append(temp_registrations[symbol])
                temp_registrations[symbol] = rows

        new_registrations.extend(temp_registrations.values())
        self._registrations = pl.DataFrame(new_registrations)

        return self

    def all_instruments(self) -> List[str]:
        return self._registrations["symbol"].unique().to_list()

    def union(self, *others: "VXInstruments") -> "VXInstruments":
        """合并另外一个股票池"""
        if len(others) == 1 and isinstance(others[0], (list, tuple)):
            others = others[0]  # type: ignore

        registrations = [self._registrations] + [
            other._registrations for other in others
        ]
        self._registrations = pl.concat(registrations)
        self.rebuild()
        return self

    def intersect(self, other: "VXInstruments") -> "VXInstruments":
        """交集"""

        new_registrations: List[Dict[str, Any]] = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            new_registrations.extend(
                {
                    "symbol": rows["symbol"],
                    "start_date": max(rows["start_date"], other_rows["start_date"]),
                    "end_date": min(rows["end_date"], other_rows["end_date"]),
                    # "weight": rows["weight"],
                }
                for other_rows in other.registrations.filter(
                    (pl.col("start_date") < rows["end_date"])
                    & (pl.col("end_date") > rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                ).iter_rows(named=True)
            )

        self._registrations = (
            pl.DataFrame(new_registrations)
            if new_registrations
            else pl.DataFrame(
                # {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                    # "weight": pl.Float64,
                },
            )
        )

        self.rebuild()
        return self

    def difference(self, other: "VXInstruments") -> "VXInstruments":
        """差集"""
        new_registrations = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            for other_rows in (
                other.registrations.filter(
                    (pl.col("start_date") <= rows["end_date"])
                    & (pl.col("end_date") >= rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                )
                .sort("start_date")
                .iter_rows(named=True)
            ):
                if rows["start_date"] < other_rows["start_date"]:
                    new_registrations.append(
                        {
                            "symbol": rows["symbol"],
                            "start_date": rows["start_date"],
                            "end_date": other_rows["start_date"] - timedelta(days=1),
                        }
                    )

                rows["start_date"] = other_rows["end_date"] + timedelta(days=1)

                if rows["start_date"] > rows["end_date"]:
                    break

            if rows["start_date"] <= rows["end_date"]:
                new_registrations.append(rows)

        self._registrations = pl.DataFrame(new_registrations)
        self.rebuild()
        return self


class VXMarketPreset:
    t0_securities = T0_ETFLOF
    cash_securities = CASH_SECURITIES

    def __init__(self, symbol: Union[str, VXSymbol]) -> None:
        symbol = symbol if isinstance(symbol, VXSymbol) else symbol_parser(symbol)
        self.symbol = default_formatter(symbol)
        data = {"symbol": self.symbol}
        if (symbol.exchange, symbol.code[:3]) in DEFULAT_SYMBOL_MAP:
            data = DEFULAT_SYMBOL_MAP[(symbol.exchange, symbol.code[:3])]
        elif (symbol.exchange, symbol.code[:2]) in DEFULAT_SYMBOL_MAP:
            data = DEFULAT_SYMBOL_MAP[(symbol.exchange, symbol.code[:2])]
        else:
            data = DEFAULT_PRESET

        if self.symbol in self.t0_securities or (self.symbol in self.cash_securities):
            data["allow_t0"] = True  # type: ignore

        for key, value in data.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f"< MarketPreset({self.symbol}):{to_json(self.__dict__)} >"


class VXTick(VXDataModel):
    """行情数据"""

    tick_id: str = Field(
        default_factory=uuid4, title="ID", description="行情ID", strict=False
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    open: float = Field(default=0.0, title="Open", description="开盘价")
    high: float = Field(default=0.0, title="High", description="最高价")
    low: float = Field(default=0.0, title="Low", description="最低价")
    yclose: float = Field(default=0.0, title="YClose", description="昨收价")
    ysettle: float = Field(default=0.0, title="YSettle", description="昨结算价")
    lasttrade: float = Field(default=0.0, title="LastTrade", description="最新价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    amount: float = Field(default=0.0, title="Amount", description="成交额")
    ask1_p: float = Field(default=0.0, title="Ask1P", description="卖一价")
    ask1_v: int = Field(default=0, title="Ask1V", description="卖一量")
    bid1_p: float = Field(default=0.0, title="Bid1P", description="买一价")
    bid1_v: int = Field(default=0, title="Bid1V", description="买一量")
    ask2_p: float = Field(default=0.0, title="Ask2P", description="卖二价")
    ask2_v: int = Field(default=0, title="Ask2V", description="卖二量")
    bid2_p: float = Field(default=0.0, title="Bid2P", description="买二价")
    bid2_v: int = Field(default=0, title="Bid2V", description="买二量")
    ask3_p: float = Field(default=0.0, title="Ask3P", description="卖三价")
    ask3_v: int = Field(default=0, title="Ask3V", description="卖三量")
    bid3_p: float = Field(default=0.0, title="Bid3P", description="买三价")
    bid3_v: int = Field(default=0, title="Bid3V", description="买三量")
    ask4_p: float = Field(default=0.0, title="Ask4P", description="卖四价")
    ask4_v: int = Field(default=0, title="Ask4V", description="卖四量")
    bid4_p: float = Field(default=0.0, title="Bid4P", description="买四价")
    bid4_v: int = Field(default=0, title="Bid4V", description="买四量")
    ask5_p: float = Field(default=0.0, title="Ask5P", description="卖五价")
    ask5_v: int = Field(default=0, title="Ask5V", description="卖五量")
    bid5_p: float = Field(default=0.0, title="Bid5P", description="买五价")
    bid5_v: int = Field(default=0, title="Bid5V", description="买五量")


class VXBar(VXDataModel):
    """k线信息"""

    bar_id: str = Field(
        default_factory=lambda: uuid4().hex,
        title="ID",
        description="K线ID",
        strict=False,
    )
    symbol: str = Field(default="", title="Symbol", description="代码")
    name: str = Field(default="", title="Name", description="名称")
    open: float = Field(default=0.0, title="Open", description="开盘价")
    high: float = Field(default=0.0, title="High", description="最高价")
    low: float = Field(default=0.0, title="Low", description="最低价")
    close: float = Field(default=0.0, title="Close", description="收盘价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    amount: float = Field(default=0.0, title="Amount", description="成交额")
    # frequency: Annotated[
    #    BarFreqType, PlainValidator(lambda x: to_enum(x, default=BarFreqType.Day1))
    # ] = Field(default="1m", title="Frequency", description="k线周期类型")


class VXExecRpt(VXDataModel):
    """成交回报"""

    execrpt_id: str = Field(
        default_factory=lambda: uuid4().hex,
        title="ID",
        description="成交ID",
        strict=False,
    )
    account_id: str = Field(
        default="", title="AccountID", description="账户ID", strict=False
    )
    order_id: str = Field(
        default="", title="OrderID", description="订单ID", strict=False
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    order_side: Annotated[
        str, PlainValidator(lambda x: to_enum(x, default=OrderSide.Buy).name)
    ] = Field(default="Buy", title="Side", description="买卖方向")
    position_effect: Annotated[
        str,
        PlainValidator(lambda x: to_enum(x, default=PositionEffect.Open).name),
    ] = Field(default="Open", title="PositionEffect", description="持仓效果")
    price: float = Field(default=0.0, title="Price", description="成交价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    commission: float = Field(default=0.0, title="Fee", description="手续费")
    execrpt_type: Annotated[
        str, PlainValidator(lambda x: to_enum(x, default=ExecType.Trade).name)
    ] = Field(default="Trade", title="ExecType", description="成交类型")
    order_remark: str = Field(default="", title="Remark", description="备注")
    strategy_id: str = Field(default="", title="StrategyID", description="策略ID")


class VXOrder(VXDataModel):
    """委托信息"""

    order_id: str = Field(default="", title="ID", description="委托ID", strict=False)

    account_id: str = Field(
        default="", title="AccountID", description="账户ID", frozen=True
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    order_side: Annotated[
        str, PlainValidator(lambda x: to_enum(x, default=OrderSide.Buy).name)
    ] = Field(default="Buy", title="Side", description="买卖方向", frozen=True)
    order_type: Annotated[
        str, PlainValidator(lambda x: to_enum(x, default=OrderType.Market).name)
    ] = Field(default="Market", title="Type", description="委托类型", frozen=True)
    position_effect: Annotated[
        str,
        PlainValidator(lambda x: to_enum(x, default=PositionEffect.Open).name),
    ] = Field(
        default="Open",
        title="PositionEffect",
        description="持仓效果",
        frozen=True,
    )
    price: float = Field(default=0.0, title="Price", description="委托价", frozen=True)
    volume: int = Field(default=0, title="Volume", description="委托量", frozen=True)

    filled_volume: int = Field(default=0, title="FilledVolume", description="成交量")
    filled_vwap: float = Field(default=0.0, title="FilledVWAP", description="成交均价")
    filled_amount: float = Field(
        default=0.0, title="FilledAmount", description="成交额"
    )
    filled_commission: float = Field(
        default=0.0, title="FilledFee", description="手续费"
    )

    status: Annotated[
        str,
        PlainValidator(lambda x: to_enum(x, default=OrderStatus.PendingNew).name),
    ] = Field(default="PendingNew", title="Status", description="委托状态")
    reject_code: Annotated[
        str,
        PlainValidator(lambda x: to_enum(x, default=OrderRejectCode.Unknown).name),
    ] = Field(default="Unknown", title="RejectCode", description="拒绝代码")
    reject_reason: str = Field(default="", title="RejectReason", description="拒绝原因")
    order_remark: str = Field(default="", title="Remark", description="备注")
    strategy_id: str = Field(default="", title="StrategyID", description="策略ID")


class VXPosition(VXDataModel):
    """持仓信息"""

    account_id: str = Field(default="", title="AccountID", description="账户ID")
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    sec_type: Annotated[
        str,
        PlainValidator(lambda x: to_enum(x, default=SecType.STOCK).name),
    ] = Field(default="STOCK", title="SecType", description="证券类型")
    currency: str = Field(default="CNY", title="Currency", description="币种")
    volume_today: int = Field(default=0, title="VolumeToday", description="今仓量")
    volume_his: int = Field(default=0, title="VolumeHis", description="昨仓量")
    frozen: int = Field(default=0, title="Frozen", description="冻结量")
    lasttrade: float = Field(default=0.0, title="LastTrade", description="最新价")
    cost: float = Field(default=0.0, title="Cost", description="持仓成本")
    allow_t0: bool = Field(default=False, title="AllowT0", description="是否允许T+0")

    def model_post_init(self, _: Any) -> None:
        self.sec_type = VXMarketPreset(symbol=self.symbol).security_type  # type: ignore
        self.allow_t0 = VXMarketPreset(symbol=self.symbol).allow_t0  # type: ignore

    @computed_field(title="Volume", description="持仓量")
    def volume(self) -> int:
        return self.volume_today + self.volume_his

    @computed_field(title="Volume", description="持仓市值")
    def market_value(self) -> float:
        return self.lasttrade * (self.volume_today + self.volume_his)

    @computed_field(title="Available", description="可用量")
    def available(self) -> int:
        return max(
            0,
            (
                (self.volume_today + self.volume_his - self.frozen)
                if self.allow_t0
                else self.volume_his - self.frozen
            ),
        )

    @computed_field(title="VWAP", description="持仓均价")
    def vwap(self) -> float:
        return (
            self.cost / (self.volume_today + self.volume_his)
            if (self.volume_today + self.volume_his) > 0
            else 0.0
        )

    @computed_field(title="PnL", description="浮动盈亏")
    def fpnl(self) -> float:
        return self.lasttrade * (self.volume_today + self.volume_his) - self.cost


class VXCashInfo(VXDataModel):
    """账户资金或负债信息"""

    account_id: str = Field(default="", title="ID", description="账户ID")
    currency: str = Field(default="CNY", title="Currency", description="币种")
    balance: float = Field(default=0.0, title="Cash", description="资金余额")
    order_frozen: float = Field(
        default=0.0, title="OrderFrozen", description="订单冻结资金"
    )
    on_way: float = Field(default=0.0, title="OnWay", description="在途资金")
    market_value: float = Field(
        default=0.0, title="MarketValue", description="持仓市值"
    )
    fpnl: float = Field(default=0.0, title="Fpnl", description="浮动盈亏")
    ynav: float = Field(default=0.0, title="YesterdayNav", description="昨日净资产")

    @computed_field(title="nav", description="总资产")
    def nav(self) -> float:
        return self.balance + self.market_value

    @computed_field(title="Available", description="可用资金")
    def available(self) -> float:
        return self.balance - self.order_frozen - self.on_way

    @computed_field(title="PnL", description="今日盈亏")
    def today_fpnl(self) -> float:
        return self.balance + self.market_value - self.ynav if self.ynav > 0 else 0.0


if __name__ == "__main__":
    tick = VXTick()
    print(tick)
    print(tick.model_dump())

    bar = VXBar()
    print(bar)
    print(bar.model_dump())

    position = VXPosition(
        symbol="SHSE.600000",
        volume_today=100,
        volume_his=100,
        frozen=10,
        # available=100,
        lasttrade=10.0,
        cost=1000.0,
    )
    print(position)
