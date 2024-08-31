from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Trade(ModelBase):
    trade_id: Optional[str] = None
    price: Optional[str] = None
    size: Optional[str] = None
    is_buyer_maker: Optional[bool] = None

    @cached_property
    def trade_id_as_int(self):
        return int(self.trade_id) if self.trade_id else None

    @cached_property
    def price_as_float(self):
        return float(self.price) if self.price else None

    @cached_property
    def price_as_decimal(self):
        return Decimal(self.price) if self.price else None

    @cached_property
    def size_as_float(self):
        return float(self.size) if self.size else None

    @cached_property
    def size_as_decimal(self):
        return Decimal(self.size) if self.size else None
