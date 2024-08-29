from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Position(ModelBase):
    quantity: Optional[str] = None
    is_long: Optional[bool] = None
    entry_price: Optional[str] = None
    mark_price: Optional[str] = None
    leverage: Optional[float] = None
    initial_margin: Optional[float] = None
    maintenance_margin: Optional[float] = None
    unrealized_pnl: Optional[float] = None
    liquidation_price: Optional[str] = None

    @cached_property
    def quantity_as_float(self):
        return float(self.quantity) if self.quantity else None

    @cached_property
    def quantity_as_decimal(self):
        return Decimal(self.quantity) if self.quantity else None

    @cached_property
    def entry_price_as_float(self):
        return float(self.entry_price) if self.entry_price else None

    @cached_property
    def entry_price_as_decimal(self):
        return Decimal(self.entry_price) if self.entry_price else None

    @cached_property
    def mark_price_as_float(self):
        return float(self.mark_price) if self.mark_price else None

    @cached_property
    def mark_price_as_decimal(self):
        return Decimal(self.mark_price) if self.mark_price else None

    @cached_property
    def liquidation_price_as_float(self):
        return float(self.liquidation_price) if self.liquidation_price else None

    @cached_property
    def liquidation_price_as_decimal(self):
        return Decimal(self.liquidation_price) if self.liquidation_price else None
