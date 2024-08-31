from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Optional

from crypto_chassis_trade.core.models.model_base import ModelBase


@dataclass(frozen=True, kw_only=True)
class Balance(ModelBase):
    quantity: Optional[str] = None  # wallet balance

    @cached_property
    def quantity_as_float(self):
        return float(self.quantity) if self.quantity else None

    @cached_property
    def quantity_as_decimal(self):
        return Decimal(self.quantity) if self.quantity else None
