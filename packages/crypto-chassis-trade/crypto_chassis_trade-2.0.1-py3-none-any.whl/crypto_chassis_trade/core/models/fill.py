from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Fill(ModelBase):
    order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    trade_id: Optional[str] = None
    is_buy: Optional[bool] = None
    price: Optional[str] = None
    quantity: Optional[str] = None

    fee_asset: Optional[str] = None
    fee_quantity: Optional[str] = None
    is_rebate: Optional[bool] = None

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
    def quantity_as_float(self):
        return float(self.quantity) if self.quantity else None

    @cached_property
    def quantity_as_decimal(self):
        return Decimal(self.quantity) if self.quantity else None

    @cached_property
    def fee_quantity_as_float(self):
        return float(self.fee_quantity) if self.fee_quantity else None

    @cached_property
    def fee_quantity_as_decimal(self):
        return Decimal(self.fee_quantity) if self.fee_quantity else None
