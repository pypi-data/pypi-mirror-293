"""网格交易策略"""

from typing import Callable, Optional
from vxquant.portfolio import VXPortfolio
from vxquant.models import VXOrder
from vxquant.base import VXBaseTdApi


class NetGrid:
    def __init__(
        self,
        account_id: str,
        symbol: str,
        base_price: float,
        up_line_method: Callable[[float], float],
        down_line_method: Callable[[float], float],
    ) -> None:
        self._account_id = account_id
        self._symbol = symbol
        self._base = 0.0
        self._up_delta = 0.01
        self._down_delta = 0.01

    @property
    def up_line(self) -> float:
        return self._base * (1 + self._up_delta)

    @property
    def down_line(self) -> float:
        return self._base * (1 - self._down_delta)

    def on_price_change(self, lasttrade: float) -> Optional[VXOrder]:
        if lasttrade > self.up_line:
            self._base = lasttrade
            return VXOrder(
                account_id=self._account_id,
                symbol=self._symbol,
                volume=100,
                price=lasttrade,
                order_side="Sell",
                order_type="Market",
                order_remark="网格交易策略卖出",
            )
        elif lasttrade < self.down_line:
            self._base = lasttrade
            return VXOrder(
                account_id=self._account_id,
                symbol=self._symbol,
                volume=100,
                price=lasttrade,
                order_side="Buy",
                order_type="Market",
                order_remark="网格交易策略买入",
            )
        return None
