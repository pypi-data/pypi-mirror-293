from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Bbo(ModelBase):
    best_bid_price: Optional[str] = None
    best_bid_size: Optional[str] = None
    best_ask_price: Optional[str] = None
    best_ask_size: Optional[str] = None

    @cached_property
    def best_bid_price_as_float(self):
        return float(self.best_bid_price) if self.best_bid_price else None

    @cached_property
    def best_bid_price_as_decimal(self):
        return Decimal(self.best_bid_price) if self.best_bid_price else None

    @cached_property
    def best_bid_size_as_float(self):
        return float(self.best_bid_size) if self.best_bid_size else None

    @cached_property
    def best_bid_size_as_decimal(self):
        return Decimal(self.best_bid_size) if self.best_bid_size else None

    @cached_property
    def best_ask_price_as_float(self):
        return float(self.best_ask_price) if self.best_ask_price else None

    @cached_property
    def best_ask_price_as_decimal(self):
        return Decimal(self.best_ask_price) if self.best_ask_price else None

    @cached_property
    def best_ask_size_as_float(self):
        return float(self.best_ask_size) if self.best_ask_size else None

    @cached_property
    def best_ask_size_as_decimal(self):
        return Decimal(self.best_ask_size) if self.best_ask_size else None
