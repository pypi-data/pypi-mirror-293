try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum  # type: ignore


from typing import Dict, List, Optional, TypeAlias

from crypto_chassis_trade.core.models.balance import Balance
from crypto_chassis_trade.core.models.bbo import Bbo
from crypto_chassis_trade.core.models.fill import Fill
from crypto_chassis_trade.core.models.instrument_information import (
    InstrumentInformation,
)
from crypto_chassis_trade.core.models.ohlcv import Ohlcv
from crypto_chassis_trade.core.models.order import Order
from crypto_chassis_trade.core.models.position import Position
from crypto_chassis_trade.core.models.trade import Trade
from crypto_chassis_trade.utility.logger_interface import LoggerInterface

Symbol: TypeAlias = str
ClientOrderId: TypeAlias = str


class ApiMethod(StrEnum):
    REST = "rest"
    WEBSOCKET = "websocket"


class MarginType(StrEnum):
    ISOLATED = "isolated"
    CROSS = "cross"


class ExchangeInterface:

    @classmethod
    def set_logger(cls, logger: LoggerInterface) -> None:
        raise NotImplementedError

    def get_all_instrument_information(self) -> Dict[Symbol, InstrumentInformation]:
        raise NotImplementedError

    def get_bbos(self) -> Dict[Symbol, Bbo]:
        raise NotImplementedError

    def get_trades(self) -> Dict[Symbol, List[Trade]]:
        # the list of Trade objects are sorted earliest to latest
        raise NotImplementedError

    def get_ohlcvs(self) -> Dict[Symbol, List[Ohlcv]]:
        # the list of Ohlcv objects are sorted earliest to latest
        raise NotImplementedError

    def get_orders(self) -> Dict[Symbol, Dict[ClientOrderId, Order]]:
        raise NotImplementedError

    def get_fills(self) -> Dict[Symbol, List[Fill]]:
        # the list of Fill objects are sorted earliest to latest
        raise NotImplementedError

    def get_positions(self) -> Dict[Symbol, Position]:
        raise NotImplementedError

    def get_balances(self) -> Dict[Symbol, Balance]:
        raise NotImplementedError

    async def start(self) -> None:
        raise NotImplementedError

    async def stop(self) -> None:
        raise NotImplementedError

    def create_order(self, *, order: Order, trade_api_method_preference: Optional[ApiMethod] = None) -> Order:
        raise NotImplementedError

    def cancel_order(self, *, symbol: str, client_order_id: str, trade_api_method_preference: Optional[ApiMethod] = None) -> None:
        raise NotImplementedError

    def cancel_orders(self, *, symbol: Optional[str] = None, trade_api_method_preference: Optional[ApiMethod] = None) -> None:
        # if symbol is not provided, it will try to cancel all open orders
        raise NotImplementedError
