from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from functools import cached_property
from typing import Any, Dict, Optional, Tuple

from crypto_chassis_trade.core.models.model_base import ModelBase


class OrderStatus(IntEnum):
    CREATE_IN_FLIGHT = 1
    CANCEL_IN_FLIGHT = 2
    CREATE_ACKNOWLEDGED = 3
    CANCEL_ACKNOWLEDGED = 4
    UNTRIGGERED = 5
    NEW = 6
    PARTIALLY_FILLED = 7
    FILLED = 8
    CANCELED = 9
    EXPIRED = 10
    REJECTED = 11


@dataclass(frozen=True, kw_only=True)
class Order(ModelBase):
    order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    is_buy: Optional[bool] = None
    price: Optional[str] = None
    quantity: Optional[str] = None

    is_post_only: Optional[bool] = False
    is_fok: Optional[bool] = False
    is_ioc: Optional[bool] = False
    is_reduce_only: Optional[bool] = False

    extra_params: Optional[Dict[str, Any]] = None

    cumulative_filled_quantity: Optional[str] = None
    cumulative_filled_quote_quantity: Optional[str] = None

    exchange_create_time_point: Optional[Tuple[int, int]] = None
    status: Optional[OrderStatus] = None

    @cached_property
    def order_id_as_int(self):
        return int(self.order_id) if self.order_id else None

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
    def cumulative_filled_quantity_as_float(self):
        return float(self.cumulative_filled_quantity) if self.cumulative_filled_quantity else None

    @cached_property
    def cumulative_filled_quantity_as_decimal(self):
        return Decimal(self.cumulative_filled_quantity) if self.cumulative_filled_quantity else None

    @cached_property
    def cumulative_filled_quote_quantity_as_float(self):
        return float(self.cumulative_filled_quote_quantity) if self.cumulative_filled_quote_quantity else None

    @cached_property
    def cumulative_filled_quote_quantity_as_decimal(self):
        return Decimal(self.cumulative_filled_quote_quantity) if self.cumulative_filled_quote_quantity else None

    @property
    def is_in_flight(self):
        return self.status <= OrderStatus.CANCEL_IN_FLIGHT

    @property
    def is_open(self):
        return self.status >= OrderStatus.CREATE_ACKNOWLEDGED and self.status <= OrderStatus.PARTIALLY_FILLED

    @property
    def is_canceled(self):
        return self.status == OrderStatus.CANCELED

    @property
    def is_closed(self):
        return self.status >= OrderStatus.FILLED
