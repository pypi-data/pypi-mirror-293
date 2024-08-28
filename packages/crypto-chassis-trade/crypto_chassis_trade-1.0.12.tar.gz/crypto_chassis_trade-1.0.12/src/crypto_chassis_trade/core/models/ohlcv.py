from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Ohlcv(ModelBase):
    start_unix_timestamp_seconds: Optional[int] = None
    open_price: Optional[str] = None
    high_price: Optional[str] = None
    low_price: Optional[str] = None
    close_price: Optional[str] = None
    volume: Optional[str] = None
    quote_volume: Optional[bool] = None

    @cached_property
    def open_price_as_float(self):
        return float(self.open_price) if self.open_price else None

    @cached_property
    def open_price_as_decimal(self):
        return Decimal(self.open_price) if self.open_price else None

    @cached_property
    def high_price_as_float(self):
        return float(self.high_price) if self.high_price else None

    @cached_property
    def high_price_as_decimal(self):
        return Decimal(self.high_price) if self.high_price else None

    @cached_property
    def low_price_as_float(self):
        return float(self.low_price) if self.low_price else None

    @cached_property
    def low_price_as_decimal(self):
        return Decimal(self.low_price) if self.low_price else None

    @cached_property
    def close_price_as_float(self):
        return float(self.close_price) if self.close_price else None

    @cached_property
    def close_price_as_decimal(self):
        return Decimal(self.close_price) if self.close_price else None

    @cached_property
    def volume_as_float(self):
        return float(self.volume) if self.volume else None

    @cached_property
    def volume_as_decimal(self):
        return Decimal(self.volume) if self.volume else None

    @cached_property
    def quote_volume_as_float(self):
        return float(self.quote_volume) if self.quote_volume else None

    @cached_property
    def quote_volume_as_decimal(self):
        return Decimal(self.quote_volume) if self.quote_volume else None
