from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class InstrumentInformation(ModelBase):
    base_asset: Optional[str] = None
    quote_asset: Optional[str] = None
    order_price_increment: Optional[str] = None
    order_quantity_increment: Optional[str] = None
    order_quantity_min: Optional[str] = None
    order_quantity_max: Optional[str] = None
    order_quote_quantity_min: Optional[str] = None
    order_quote_quantity_max: Optional[str] = None
    margin_asset: Optional[str] = None
    underlying_symbol: Optional[str] = None
    contract_size: Optional[str] = None
    contract_multiplier: Optional[str] = None
    expiry_time: Optional[int] = None
    is_open_for_trade: Optional[bool] = None

    @cached_property
    def order_price_increment_as_float(self):
        return float(self.order_price_increment) if self.order_price_increment else None

    @cached_property
    def order_price_increment_as_decimal(self):
        return Decimal(self.order_price_increment) if self.order_price_increment else None

    @cached_property
    def order_quantity_increment_as_float(self):
        return float(self.order_quantity_increment) if self.order_quantity_increment else None

    @cached_property
    def order_quantity_increment_as_decimal(self):
        return Decimal(self.order_quantity_increment) if self.order_quantity_increment else None

    @cached_property
    def order_quantity_min_as_float(self):
        return float(self.order_quantity_min) if self.order_quantity_min else None

    @cached_property
    def order_quantity_min_as_decimal(self):
        return Decimal(self.order_quantity_min) if self.order_quantity_min else None

    @cached_property
    def order_quantity_max_as_float(self):
        return float(self.order_quantity_max) if self.order_quantity_max else None

    @cached_property
    def order_quantity_max_as_decimal(self):
        return Decimal(self.order_quantity_max) if self.order_quantity_max else None

    @cached_property
    def order_quote_quantity_min_as_float(self):
        return float(self.order_quote_quantity_min) if self.order_quote_quantity_min else None

    @cached_property
    def order_quote_quantity_min_as_decimal(self):
        return Decimal(self.order_quote_quantity_min) if self.order_quote_quantity_min else None

    @cached_property
    def order_quote_quantity_max_as_float(self):
        return float(self.order_quote_quantity_max) if self.order_quote_quantity_max else None

    @cached_property
    def order_quote_quantity_max_as_decimal(self):
        return Decimal(self.order_quote_quantity_max) if self.order_quote_quantity_max else None

    @cached_property
    def contract_size_as_float(self):
        return float(self.contract_size) if self.contract_size else None

    @cached_property
    def contract_size_as_decimal(self):
        return Decimal(self.contract_size) if self.contract_size else None

    @cached_property
    def contract_multiplier_as_float(self):
        return float(self.contract_multiplier) if self.contract_multiplier else None

    @cached_property
    def contract_multiplier_as_decimal(self):
        return Decimal(self.contract_multiplier) if self.contract_multiplier else None
