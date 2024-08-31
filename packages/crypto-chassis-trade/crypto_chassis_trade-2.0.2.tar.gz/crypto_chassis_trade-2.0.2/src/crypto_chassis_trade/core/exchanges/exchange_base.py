import asyncio
import dataclasses
import functools
from decimal import Decimal
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, TypeAlias

import aiohttp

from crypto_chassis_trade.core.exchanges.exchange_interface import (
    ApiMethod,
    ExchangeInterface,
    MarginType,
)
from crypto_chassis_trade.core.models.balance import Balance
from crypto_chassis_trade.core.models.bbo import Bbo
from crypto_chassis_trade.core.models.fill import Fill
from crypto_chassis_trade.core.models.instrument_information import (
    InstrumentInformation,
)
from crypto_chassis_trade.core.models.ohlcv import Ohlcv
from crypto_chassis_trade.core.models.order import Order, OrderStatus
from crypto_chassis_trade.core.models.position import Position
from crypto_chassis_trade.core.models.trade import Trade
from crypto_chassis_trade.core.network.rest_request import RestRequest
from crypto_chassis_trade.core.network.rest_response import RestResponse
from crypto_chassis_trade.core.network.websocket_connection import WebsocketConnection
from crypto_chassis_trade.core.network.websocket_message import WebsocketMessage
from crypto_chassis_trade.core.network.websocket_request import WebsocketRequest
from crypto_chassis_trade.utility.helper import (
    convert_set_to_subsets,
    convert_time_point_delta_to_seconds,
    create_url,
    create_url_with_query_params,
    time_point_now,
    time_point_subtract,
    unix_timestamp_milliseconds_now,
    unix_timestamp_seconds_now,
)
from crypto_chassis_trade.utility.logger import Logger
from crypto_chassis_trade.utility.logger_interface import LoggerInterface

Symbol: TypeAlias = str
ClientOrderId: TypeAlias = str


class ExchangeBase(ExchangeInterface):

    logger: LoggerInterface = Logger()

    @classmethod
    def set_logger(cls, logger: LoggerInterface) -> None:
        ExchangeBase.logger = logger

    def __init__(
        self,
        *,
        name: str,
        symbols: str | Iterable[str],  # a comma-separated string or an iterable of strings. Use '*' to represent all symbols that are open for trade.
        instrument_type: Optional[str] = None,  # Defaults to spot type. See each derived exchange class for allowed values for that exchange.
        # bbo
        subscribe_bbo: bool = False,
        # trade
        subscribe_trade: bool = False,
        fetch_historical_trade_at_start: bool = False,
        fetch_historical_trade_start_unix_timestamp_seconds: Optional[int] = None,
        fetch_historical_trade_end_unix_timestamp_seconds: Optional[int] = None,
        keep_historical_trade_seconds: Optional[int] = 300,  # max historical data time span
        prune_historical_trade_interval_seconds: Optional[int] = 60,  # how often to prune
        # ohlcv
        subscribe_ohlcv: bool = False,
        ohlcv_interval_seconds: int = 60,
        fetch_historical_ohlcv_at_start: bool = False,
        fetch_historical_ohlcv_start_unix_timestamp_seconds: Optional[int] = None,
        fetch_historical_ohlcv_end_unix_timestamp_seconds: Optional[int] = None,
        keep_historical_ohlcv_seconds: Optional[int] = 300,  # max historical data time span
        prune_historical_ohlcv_interval_seconds: Optional[int] = 60,  # how often to prune
        # account
        is_demo_trading: bool = False,
        api_key: str = "",
        api_secret: str = "",
        api_passphrase: str = "",
        margin_type: Optional[MarginType] = None,
        # order
        subscribe_order: bool = False,
        fetch_historical_order_at_start: bool = False,
        fetch_historical_order_start_unix_timestamp_seconds: Optional[int] = None,
        fetch_historical_order_end_unix_timestamp_seconds: Optional[int] = None,
        keep_historical_order_seconds: Optional[int] = 300,  # max historical data time span
        prune_historical_order_interval_seconds: Optional[int] = 60,  # how often to prune
        # fill
        subscribe_fill: bool = False,
        fetch_historical_fill_at_start: bool = False,
        fetch_historical_fill_start_unix_timestamp_seconds: Optional[int] = None,
        fetch_historical_fill_end_unix_timestamp_seconds: Optional[int] = None,
        keep_historical_fill_seconds: Optional[int] = 300,  # max historical data time span
        prune_historical_fill_interval_seconds: Optional[int] = 60,  # how often to prune
        # position
        subscribe_position: bool = False,
        # balance
        subscribe_balance: bool = False,
        # settings for using REST API to periodically sync data with the exchange
        rest_market_data_fetch_all_instrument_information_at_start: bool = True,
        rest_market_data_fetch_all_instrument_information_period_seconds: Optional[int] = 300,
        rest_market_data_fetch_bbo_period_seconds: Optional[int] = 300,
        rest_account_check_open_order_period_seconds: Optional[int] = 60,
        rest_account_check_open_order_threshold_seconds: Optional[int] = 60,
        rest_account_check_in_flight_order_period_seconds: Optional[int] = 10,
        rest_account_check_in_flight_order_threshold_seconds: Optional[int] = 10,
        rest_account_fetch_position_period_seconds: Optional[int] = 60,
        rest_account_fetch_balance_period_seconds: Optional[int] = 60,
        rest_market_data_send_consecutive_request_delay_seconds: Optional[
            float
        ] = 0.05,  # only applicable to paginated requests such as fetching historical data
        rest_account_send_consecutive_request_delay_seconds: Optional[float] = 0.05,  # only applicable to paginated requests such as fetching historical data
        # settings for using Websocket API to stream realtime data from the exchange
        websocket_connection_protocol_level_heartbeat_period_seconds: Optional[int] = 10,
        websocket_connection_application_level_heartbeat_period_seconds: Optional[int] = 10,
        websocket_connection_application_level_heartbeat_timeout_seconds: Optional[int] = 20,
        websocket_connection_auto_reconnect: bool = True,
        websocket_market_data_channel_symbols_limit: Optional[int] = 50,
        websocket_market_data_channel_send_consecutive_request_delay_seconds: Optional[
            float
        ] = 0.05,  # only applicable to divided requests such as subscribing on many symbols
        # which API method is preferred to create/cancel orders
        trade_api_method_preference: Optional[ApiMethod] = ApiMethod.REST,
        extra_data: Any = None,  # arbitrary user-defined data
        start_wait_seconds: int = 1,  # wait time at start
        stop_wait_seconds: int = 1,  # wait time at stop
        client_session: Optional[aiohttp.ClientSession] = None,
        json_serialize: Optional[Callable[[Any], str]] = None,  # function to serialize json
        json_deserialize: Optional[Callable[[str], Any]] = None,  # function to deserialize json
    ):
        # data obtained from and synced with the exchange
        self.all_instrument_information: Dict[Symbol, InstrumentInformation] = {}
        self.bbos: Dict[Symbol, Bbo] = {}
        self.trades: Dict[Symbol, List[Trade]] = {}  # the list of Trade objects are sorted earliest to latest
        self.ohlcvs: Dict[Symbol, List[Ohlcv]] = {}  # the list of Ohlcv objects are sorted earliest to latest
        self.orders: Dict[Symbol, Dict[ClientOrderId, Order]] = {}
        self.fills: Dict[Symbol, List[Fill]] = {}  # the list of Fill objects are sorted earliest to latest
        self.positions: Dict[Symbol, Position] = {}
        self.balances: Dict[Symbol, Balance] = {}

        now_unix_timestamp_seconds = unix_timestamp_seconds_now()
        self.name = name

        if isinstance(symbols, str):
            self.symbols = set((y for x in symbols.split(",") if (y := x.strip())))
        else:
            self.symbols = set(symbols)

        self.instrument_type = instrument_type
        if not self.is_instrument_type_valid(instrument_type=instrument_type):
            ExchangeBase.logger.critical(Exception(f"invalid instrument_type {instrument_type} for exchange {self.name}"))

        self.subscribe_bbo = subscribe_bbo

        self.subscribe_trade = subscribe_trade
        self.fetch_historical_trade_at_start = fetch_historical_trade_at_start
        self.fetch_historical_trade_start_unix_timestamp_seconds = fetch_historical_trade_start_unix_timestamp_seconds
        self.fetch_historical_trade_end_unix_timestamp_seconds = (
            fetch_historical_trade_end_unix_timestamp_seconds if fetch_historical_trade_end_unix_timestamp_seconds is not None else now_unix_timestamp_seconds
        )
        self.keep_historical_trade_seconds = keep_historical_trade_seconds
        self.prune_historical_trade_interval_seconds = prune_historical_trade_interval_seconds

        self.ohlcv_interval_seconds = ohlcv_interval_seconds
        self.subscribe_ohlcv = subscribe_ohlcv
        self.fetch_historical_ohlcv_at_start = fetch_historical_ohlcv_at_start
        self.fetch_historical_ohlcv_start_unix_timestamp_seconds = fetch_historical_ohlcv_start_unix_timestamp_seconds
        self.fetch_historical_ohlcv_end_unix_timestamp_seconds = (
            fetch_historical_ohlcv_end_unix_timestamp_seconds if fetch_historical_ohlcv_end_unix_timestamp_seconds is not None else now_unix_timestamp_seconds
        )
        self.keep_historical_ohlcv_seconds = keep_historical_ohlcv_seconds
        self.prune_historical_ohlcv_interval_seconds = prune_historical_ohlcv_interval_seconds

        self.is_demo_trading = is_demo_trading
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.margin_type = margin_type

        self.subscribe_order = subscribe_order
        self.fetch_historical_order_at_start = fetch_historical_order_at_start
        self.fetch_historical_order_start_unix_timestamp_seconds = fetch_historical_order_start_unix_timestamp_seconds
        self.fetch_historical_order_end_unix_timestamp_seconds = (
            fetch_historical_order_end_unix_timestamp_seconds if fetch_historical_order_end_unix_timestamp_seconds is not None else now_unix_timestamp_seconds
        )
        self.keep_historical_order_seconds = keep_historical_order_seconds
        self.prune_historical_order_interval_seconds = prune_historical_order_interval_seconds

        self.subscribe_fill = subscribe_fill
        self.fetch_historical_fill_at_start = fetch_historical_fill_at_start
        self.fetch_historical_fill_start_unix_timestamp_seconds = fetch_historical_fill_start_unix_timestamp_seconds
        self.fetch_historical_fill_end_unix_timestamp_seconds = (
            fetch_historical_fill_end_unix_timestamp_seconds if fetch_historical_fill_end_unix_timestamp_seconds is not None else now_unix_timestamp_seconds
        )
        self.keep_historical_fill_seconds = keep_historical_fill_seconds
        self.prune_historical_fill_interval_seconds = prune_historical_fill_interval_seconds

        self.subscribe_position = subscribe_position

        self.subscribe_balance = subscribe_balance

        self.rest_market_data_fetch_all_instrument_information_at_start = rest_market_data_fetch_all_instrument_information_at_start
        self.rest_market_data_fetch_all_instrument_information_period_seconds = rest_market_data_fetch_all_instrument_information_period_seconds
        self.rest_market_data_fetch_bbo_period_seconds = rest_market_data_fetch_bbo_period_seconds
        self.rest_account_check_open_order_period_seconds = rest_account_check_open_order_period_seconds
        self.rest_account_check_open_order_threshold_seconds = rest_account_check_open_order_threshold_seconds
        self.rest_account_check_in_flight_order_period_seconds = rest_account_check_in_flight_order_period_seconds
        self.rest_account_check_in_flight_order_threshold_seconds = rest_account_check_in_flight_order_threshold_seconds
        self.rest_account_fetch_position_period_seconds = rest_account_fetch_position_period_seconds
        self.rest_account_fetch_balance_period_seconds = rest_account_fetch_balance_period_seconds
        self.rest_market_data_send_consecutive_request_delay_seconds = rest_market_data_send_consecutive_request_delay_seconds
        self.rest_account_send_consecutive_request_delay_seconds = rest_account_send_consecutive_request_delay_seconds

        self.websocket_connection_protocol_level_heartbeat_period_seconds = websocket_connection_protocol_level_heartbeat_period_seconds
        self.websocket_connection_application_level_heartbeat_period_seconds = websocket_connection_application_level_heartbeat_period_seconds
        self.websocket_connection_application_level_heartbeat_timeout_seconds = websocket_connection_application_level_heartbeat_timeout_seconds
        self.websocket_connection_auto_reconnect = websocket_connection_auto_reconnect
        self.reset_websocket_reconnect_delay_delay_seconds = 60
        self.websocket_reconnect_delay_seconds_exponential_backoff_initial = 1
        self.websocket_reconnect_delay_seconds_exponential_backoff_base = 2
        self.websocket_reconnect_delay_seconds_exponential_backoff_max = 60
        self.websocket_market_data_channel_symbols_limit = websocket_market_data_channel_symbols_limit
        self.websocket_market_data_channel_send_consecutive_request_delay_seconds = websocket_market_data_channel_send_consecutive_request_delay_seconds

        self.trade_api_method_preference = trade_api_method_preference

        self.extra_data = extra_data
        self.start_wait_seconds = start_wait_seconds
        self.stop_wait_seconds = stop_wait_seconds

        self.client_session = client_session if client_session else aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        self.close_client_session_at_stop = not client_session

        if json_serialize:
            self.json_serialize = json_serialize
        else:
            import json

            self.json_serialize = json.dumps

        if json_deserialize:
            self.json_deserialize = json_deserialize
        else:
            import json

            self.json_deserialize = functools.partial(json.loads, parse_float=lambda x: x, parse_int=lambda x: x)

        self.rest_market_data_base_url: Optional[str] = None
        self.rest_account_base_url: Optional[str] = None
        self.rest_market_data_fetch_all_instrument_information_path: Optional[str] = None
        self.rest_market_data_fetch_bbo_path: Optional[str] = None
        self.rest_market_data_fetch_historical_trade_path: Optional[str] = None
        self.rest_market_data_fetch_historical_trade_limit: Optional[int] = None
        self.rest_market_data_fetch_historical_ohlcv_path: Optional[str] = None
        self.rest_market_data_fetch_historical_ohlcv_limit: Optional[int] = None
        self.rest_account_create_order_path: Optional[str] = None
        self.rest_account_cancel_order_path: Optional[str] = None
        self.rest_account_fetch_order_path: Optional[str] = None
        self.rest_account_fetch_open_order_path: Optional[str] = None
        self.rest_account_fetch_open_order_limit: Optional[int] = None
        self.rest_account_fetch_position_path: Optional[str] = None
        self.rest_account_fetch_balance_path: Optional[str] = None
        self.rest_account_fetch_historical_order_path: Optional[str] = None
        self.rest_account_fetch_historical_order_limit: Optional[int] = None
        self.rest_account_fetch_historical_fill_path: Optional[str] = None
        self.rest_account_fetch_historical_fill_limit: Optional[int] = None

        self.websocket_market_data_base_url: Optional[str] = None
        self.websocket_account_base_url: Optional[str] = None
        self.websocket_market_data_path: Optional[str] = None
        self.websocket_market_data_query_params: Optional[Dict[str, str | int]] = None
        self.websocket_market_data_channel_bbo: Optional[str] = None
        self.websocket_market_data_channel_trade: Optional[str] = None
        self.websocket_market_data_channel_ohlcv: Optional[str] = None
        self.websocket_account_path: Optional[str] = None
        self.websocket_account_query_params: Optional[Dict[str, str | int]] = None
        self.websocket_account_channel_order: Optional[str] = None
        self.websocket_account_channel_fill: Optional[str] = None
        self.websocket_account_channel_position: Optional[str] = None
        self.websocket_account_channel_balance: Optional[str] = None
        self.websocket_account_trade_base_url: Optional[str] = None
        self.websocket_account_trade_path: Optional[str] = None
        self.websocket_account_trade_query_params: Optional[Dict[str, str | int]] = None

        self.order_status_mapping: Dict[str, OrderStatus] = {}

        self.broker_id: Optional[str] = None

        self.next_rest_request_id_int: int = 0
        self.next_websocket_request_id_int: int = 0
        self.last_client_order_id_unix_timestamp_milliseconds: Optional[int] = None
        self.last_client_order_id_sequence_number: Optional[int] = None

        self.websocket_connections: Dict[str, WebsocketConnection] = {}
        self.websocket_reconnect_delay_seconds: Dict[str, int] = {}
        self.websocket_logged_in_connections: Set[str] = set()
        self.websocket_requests: Dict[str, WebsocketRequest] = {}

        self.all_tasks: List[asyncio.Task] = []
        self.stopped = False

    def get_all_instrument_information(self) -> Dict[Symbol, InstrumentInformation]:
        return self.all_instrument_information

    def get_bbos(self) -> Dict[Symbol, Bbo]:
        return self.bbos

    def get_trades(self) -> Dict[Symbol, List[Trade]]:
        return self.trades

    def get_ohlcvs(self) -> Dict[Symbol, List[Ohlcv]]:
        return self.ohlcvs

    def get_orders(self) -> Dict[Symbol, Dict[ClientOrderId, Order]]:
        return self.orders

    def get_fills(self) -> Dict[Symbol, List[Fill]]:
        return self.fills

    def get_positions(self) -> Dict[Symbol, Position]:
        return self.positions

    def get_balances(self) -> Dict[Symbol, Balance]:
        return self.balances

    async def start(self):
        ExchangeBase.logger.info("starting...")

        if self.rest_market_data_fetch_all_instrument_information_at_start:
            await self.rest_market_data_fetch_all_instrument_information()
            if "*" in self.symbols:
                self.symbols = {
                    symbol for symbol, instrument_information in self.all_instrument_information.items() if instrument_information.is_open_for_trade
                }

        if self.rest_market_data_fetch_all_instrument_information_period_seconds:

            async def start_periodic_rest_market_data_fetch_all_instrument_information():
                try:
                    while True:
                        await asyncio.sleep(self.rest_market_data_fetch_all_instrument_information_period_seconds)
                        await self.rest_market_data_fetch_all_instrument_information()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_market_data_fetch_all_instrument_information()))

        if self.subscribe_bbo:
            await self.rest_market_data_fetch_bbo()

        if self.rest_market_data_fetch_bbo_period_seconds:

            async def start_periodic_rest_market_data_fetch_bbo():
                try:
                    while True:
                        await asyncio.sleep(self.rest_market_data_fetch_bbo_period_seconds)
                        await self.rest_market_data_fetch_bbo()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_market_data_fetch_bbo()))

        if self.subscribe_order:
            await self.rest_account_fetch_open_order()

        if self.rest_account_check_open_order_period_seconds:

            async def start_periodic_rest_account_check_open_order():
                try:
                    while True:
                        await asyncio.sleep(self.rest_account_check_open_order_period_seconds)
                        await self.rest_account_check_open_order()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_account_check_open_order()))

        if self.rest_account_check_in_flight_order_period_seconds:

            async def start_periodic_rest_account_check_in_flight_order():
                try:
                    while True:
                        await asyncio.sleep(self.rest_account_check_in_flight_order_period_seconds)
                        await self.rest_account_check_in_flight_order()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_account_check_in_flight_order()))

        if self.subscribe_position:
            await self.rest_account_fetch_position()

        if self.rest_account_fetch_position_period_seconds:

            async def start_periodic_rest_account_fetch_position():
                try:
                    while True:
                        await asyncio.sleep(self.rest_account_fetch_position_period_seconds)
                        await self.rest_account_fetch_position()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_account_fetch_position()))

        if self.subscribe_balance:
            await self.rest_account_fetch_balance()

        if self.rest_account_fetch_balance_period_seconds:

            async def start_periodic_rest_account_fetch_balance():
                try:
                    while True:
                        await asyncio.sleep(self.rest_account_fetch_balance_period_seconds)
                        await self.rest_account_fetch_balance()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_rest_account_fetch_balance()))

        if self.prune_historical_trade_interval_seconds:

            async def start_periodic_prune_historical_trade():
                try:
                    while True:
                        await asyncio.sleep(self.prune_historical_trade_interval_seconds)
                        self.prune_trades()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_prune_historical_trade()))

        if self.prune_historical_ohlcv_interval_seconds:

            async def start_periodic_prune_historical_ohlcv():
                try:
                    while True:
                        await asyncio.sleep(self.prune_historical_ohlcv_interval_seconds)
                        self.prune_ohlcvs()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_prune_historical_ohlcv()))

        if self.prune_historical_order_interval_seconds:

            async def start_periodic_prune_historical_order():
                try:
                    while True:
                        await asyncio.sleep(self.prune_historical_order_interval_seconds)
                        self.prune_orders()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_prune_historical_order()))

        if self.prune_historical_fill_interval_seconds:

            async def start_periodic_prune_historical_fill():
                try:
                    while True:
                        await asyncio.sleep(self.prune_historical_fill_interval_seconds)
                        self.prune_fills()
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_periodic_prune_historical_fill()))

        await asyncio.gather(self.websocket_market_data_connect(), self.websocket_account_connect())
        await asyncio.gather(self.rest_market_data_fetch_historical_data(), self.rest_account_fetch_historical_data())

        if self.websocket_connection_application_level_heartbeat_period_seconds:

            async def start_websocket_connection_ping_on_application_level():
                try:
                    while True:
                        await asyncio.sleep(self.websocket_connection_application_level_heartbeat_period_seconds)
                        for websocket_connection in list(self.websocket_connections.values()):
                            try:
                                if not websocket_connection.connection.closed:
                                    await self.send_websocket_request(
                                        websocket_connection=websocket_connection,
                                        websocket_request=self.websocket_connection_ping_on_application_level_create_websocket_request(),
                                    )
                            except Exception as exception:
                                ExchangeBase.logger.error(exception)
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_websocket_connection_ping_on_application_level()))

        if self.websocket_connection_application_level_heartbeat_timeout_seconds:

            async def start_websocket_connection_application_level_heartbeat_timeout():
                try:
                    while True:
                        await asyncio.sleep(self.websocket_connection_application_level_heartbeat_timeout_seconds)
                        for websocket_connection in list(self.websocket_connections.values()):
                            try:
                                if not websocket_connection.connection.closed:
                                    now_time_point = time_point_now()
                                    if (
                                        websocket_connection.latest_receive_message_time_point
                                        and convert_time_point_delta_to_seconds(
                                            time_point_delta=time_point_subtract(
                                                time_point_1=now_time_point, time_point_2=websocket_connection.latest_receive_message_time_point
                                            )
                                        )
                                        > self.websocket_connection_application_level_heartbeat_timeout_seconds
                                    ):
                                        await websocket_connection.connection.close(message=b"application level heartbeat timeout")
                            except Exception as exception:
                                ExchangeBase.logger.error(exception)
                except Exception as exception:
                    ExchangeBase.logger.error(exception)

            self.all_tasks.append(asyncio.create_task(start_websocket_connection_application_level_heartbeat_timeout()))

        await asyncio.sleep(self.start_wait_seconds)

        ExchangeBase.logger.info("started")

    async def stop(self):
        ExchangeBase.logger.info("stopping...")

        self.stopped = True

        for websocket_connection in list(self.websocket_connections.values()):
            if not websocket_connection.connection.closed:
                await websocket_connection.connection.close()

        for task in self.all_tasks:
            task.cancel()

        await asyncio.gather(*self.all_tasks, return_exceptions=True)

        if self.close_client_session_at_stop:
            await self.client_session.close()

        await asyncio.sleep(self.stop_wait_seconds)

        ExchangeBase.logger.info("stopped")

    def create_order(self, *, order, trade_api_method_preference=None):
        order_to_create = self.create_order_ensure_client_order_id(order=order)

        self.upsert_order(order=order_to_create)

        if (
            (trade_api_method_preference is None and (self.trade_api_method_preference is None or self.trade_api_method_preference == ApiMethod.REST))
            or trade_api_method_preference == ApiMethod.REST
            or self.websocket_account_trade_url_with_query_params not in self.websocket_logged_in_connections
        ):
            self.all_tasks.append(asyncio.create_task(self.rest_account_create_order(order=order_to_create)))
        else:
            self.all_tasks.append(
                asyncio.create_task(
                    self.websocket_account_create_order(
                        websocket_connection=self.websocket_connections[self.websocket_account_trade_url_with_query_params], order=order_to_create
                    )
                )
            )

        return order_to_create

    def create_order_ensure_client_order_id(self, *, order):
        if not order.client_order_id:
            return dataclasses.replace(
                order, exchange_update_time_point=time_point_now(), status=OrderStatus.CREATE_IN_FLIGHT, client_order_id=self.generate_next_client_order_id()
            )
        else:
            return dataclasses.replace(order, exchange_update_time_point=time_point_now(), status=OrderStatus.CREATE_IN_FLIGHT)

    def cancel_order(self, *, symbol, client_order_id, trade_api_method_preference=None):
        self.replace_order(symbol=symbol, client_order_id=client_order_id, exchange_update_time_point=time_point_now(), status=OrderStatus.CANCEL_IN_FLIGHT)

        if (
            (trade_api_method_preference is None and (self.trade_api_method_preference is None or self.trade_api_method_preference == ApiMethod.REST))
            or trade_api_method_preference == ApiMethod.REST
            or self.websocket_account_trade_url_with_query_params not in self.websocket_logged_in_connections
        ):
            self.all_tasks.append(asyncio.create_task(self.rest_account_cancel_order(symbol=symbol, client_order_id=client_order_id)))
        else:
            self.all_tasks.append(
                asyncio.create_task(
                    self.websocket_account_cancel_order(
                        websocket_connection=self.websocket_connections[self.websocket_account_trade_url_with_query_params],
                        symbol=symbol,
                        client_order_id=client_order_id,
                    )
                )
            )

    def cancel_orders(self, *, symbol=None, trade_api_method_preference=None):
        if symbol:
            if symbol in self.orders:
                for client_order_id, order in self.orders[symbol].items():
                    if not order.is_in_flight and order.is_open:
                        self.cancel_order(symbol=symbol, client_order_id=client_order_id, trade_api_method_preference=trade_api_method_preference)
            else:
                ExchangeBase.logger.warning(f"symbol {symbol} not found in self.orders", self.orders)
        else:
            for symbol, orders_for_symbol in self.orders.items():
                for client_order_id, order in orders_for_symbol.items():
                    if not order.is_in_flight and order.is_open:
                        self.cancel_order(symbol=symbol, client_order_id=client_order_id, trade_api_method_preference=trade_api_method_preference)

    def is_instrument_type_valid(self, *, instrument_type):
        return True

    async def send_rest_request(self, *, rest_request_function, delay_seconds=0, timeout_seconds=10):
        next_rest_request_function = rest_request_function
        next_rest_request_delay_seconds = delay_seconds
        while True:
            if next_rest_request_delay_seconds:
                await asyncio.sleep(next_rest_request_delay_seconds)

            rest_request = next_rest_request_function(time_point=time_point_now())
            ExchangeBase.logger.detail("rest_request", rest_request)

            async with self.client_session.request(
                method=rest_request.method,
                url=rest_request.url,
                params=rest_request.query_string,
                data=rest_request.payload,
                headers=rest_request.headers,
                timeout=aiohttp.ClientTimeout(sock_read=timeout_seconds),
            ) as client_response:
                try:
                    raw_rest_response = client_response
                    rest_response = await self.rest_on_response(rest_request=rest_request, raw_rest_response=raw_rest_response)
                    ExchangeBase.logger.detail("rest_response", rest_response)

                    if not rest_response or rest_response.next_rest_request_function is None:
                        break
                    else:
                        next_rest_request_function = rest_response.next_rest_request_function
                        next_rest_request_delay_seconds = rest_response.next_rest_request_delay_seconds

                except Exception as exception:
                    ExchangeBase.logger.error(exception)
                    break

    async def rest_on_response(self, *, rest_request, raw_rest_response):
        raw_rest_response_text = await raw_rest_response.text()
        ExchangeBase.logger.trace("raw_rest_response_text", raw_rest_response_text)
        rest_response = RestResponse(
            rest_request=rest_request,
            status_code=raw_rest_response.status,
            payload=raw_rest_response_text,
            headers=raw_rest_response.headers,
            json_deserialize=self.json_deserialize,
        )
        rest_response.json_deserialized_payload

        if self.is_rest_response_success(rest_response=rest_response):
            if self.is_rest_response_for_all_instrument_information(rest_response=rest_response):
                await self.handle_rest_response_for_all_instrument_information(rest_response=rest_response)

            elif self.is_rest_response_for_bbo(rest_response=rest_response):
                await self.handle_rest_response_for_bbo(rest_response=rest_response)

            elif self.is_rest_response_for_historical_trade(rest_response=rest_response):
                rest_response = await self.handle_rest_response_for_historical_trade(rest_response=rest_response)

            elif self.is_rest_response_for_historical_ohlcv(rest_response=rest_response):
                rest_response = await self.handle_rest_response_for_historical_ohlcv(rest_response=rest_response)

            elif self.is_rest_response_for_create_order(rest_response=rest_response):
                await self.handle_rest_response_for_create_order(rest_response=rest_response)

            elif self.is_rest_response_for_cancel_order(rest_response=rest_response):
                await self.handle_rest_response_for_cancel_order(rest_response=rest_response)

            elif self.is_rest_response_for_fetch_order(rest_response=rest_response):
                await self.handle_rest_response_for_fetch_order(rest_response=rest_response)

            elif self.is_rest_response_for_fetch_open_order(rest_response=rest_response):
                rest_response = await self.handle_rest_response_for_fetch_open_order(rest_response=rest_response)

            elif self.is_rest_response_for_fetch_position(rest_response=rest_response):
                await self.handle_rest_response_for_fetch_position(rest_response=rest_response)

            elif self.is_rest_response_for_fetch_balance(rest_response=rest_response):
                await self.handle_rest_response_for_fetch_balance(rest_response=rest_response)

            elif self.is_rest_response_for_historical_order(rest_response=rest_response):
                rest_response = await self.handle_rest_response_for_historical_order(rest_response=rest_response)

            elif self.is_rest_response_for_historical_fill(rest_response=rest_response):
                rest_response = await self.handle_rest_response_for_historical_fill(rest_response=rest_response)

        else:
            rest_response = await self.handle_rest_response_for_error(rest_response=rest_response)

        return rest_response

    async def rest_market_data_fetch_all_instrument_information(self):
        await self.send_rest_request(rest_request_function=self.rest_market_data_fetch_all_instrument_information_create_rest_request_function())

    async def rest_market_data_fetch_bbo(self):
        await self.send_rest_request(rest_request_function=self.rest_market_data_fetch_bbo_create_rest_request_function())

    async def rest_market_data_fetch_historical_data(self):
        for symbol in sorted(self.symbols):
            if self.fetch_historical_trade_at_start:
                await self.rest_market_data_fetch_historical_trade(symbol=symbol)
            if self.fetch_historical_ohlcv_at_start:
                await self.rest_market_data_fetch_historical_ohlcv(symbol=symbol)

    async def rest_market_data_fetch_historical_trade(self, *, symbol):
        await self.send_rest_request(rest_request_function=self.rest_market_data_fetch_historical_trade_create_rest_request_function(symbol=symbol))

    async def rest_market_data_fetch_historical_ohlcv(self, *, symbol):
        await self.send_rest_request(rest_request_function=self.rest_market_data_fetch_historical_ohlcv_create_rest_request_function(symbol=symbol))

    async def rest_account_create_order(self, *, order):
        try:
            order_to_create = self.create_order_ensure_client_order_id(order=order)
            await self.send_rest_request(rest_request_function=self.rest_account_create_order_create_rest_request_function(order=order_to_create))
            return self.orders[order_to_create.symbol][order_to_create.client_order_id]
        except Exception as exception:
            ExchangeBase.logger.error(exception)

    async def rest_account_cancel_order(self, *, symbol, client_order_id):
        try:
            await self.send_rest_request(
                rest_request_function=self.rest_account_cancel_order_create_rest_request_function(symbol=symbol, client_order_id=client_order_id)
            )
        except Exception as exception:
            ExchangeBase.logger.error(exception)

    async def rest_account_fetch_order(self, *, symbol, client_order_id):
        await self.send_rest_request(
            rest_request_function=self.rest_account_fetch_order_create_rest_request_function(symbol=symbol, client_order_id=client_order_id)
        )

    async def rest_account_fetch_open_order(self):
        await self.send_rest_request(rest_request_function=self.rest_account_fetch_open_order_create_rest_request_function())

    async def rest_account_fetch_position(self):
        await self.send_rest_request(rest_request_function=self.rest_account_fetch_position_create_rest_request_function())

    async def rest_account_fetch_balance(self):
        await self.send_rest_request(rest_request_function=self.rest_account_fetch_balance_create_rest_request_function())

    async def rest_account_check_open_order(self):
        for symbol, orders_for_symbol in self.orders.items():
            for client_order_id, order in orders_for_symbol.items():
                now_time_point = time_point_now()
                if (
                    order.is_open
                    and convert_time_point_delta_to_seconds(
                        time_point_delta=time_point_subtract(time_point_1=now_time_point, time_point_2=order.exchange_update_time_point)
                    )
                    > self.rest_account_check_open_order_threshold_seconds
                ):
                    await self.rest_account_fetch_order(symbol=symbol, client_order_id=client_order_id)
                    await asyncio.sleep(self.rest_account_send_consecutive_request_delay_seconds)

    async def rest_account_check_in_flight_order(self):
        for symbol, orders_for_symbol in self.orders.items():
            for client_order_id, order in orders_for_symbol.items():
                now_time_point = time_point_now()
                if (
                    order.is_in_flight
                    and convert_time_point_delta_to_seconds(
                        time_point_delta=time_point_subtract(time_point_1=now_time_point, time_point_2=order.exchange_update_time_point)
                    )
                    > self.rest_account_check_in_flight_order_threshold_seconds
                ):
                    await self.rest_account_fetch_order(symbol=symbol, client_order_id=client_order_id)
                    await asyncio.sleep(self.rest_account_send_consecutive_request_delay_seconds)

    async def rest_account_fetch_historical_data(self):
        for symbol in sorted(self.symbols):
            if self.fetch_historical_order_at_start:
                await self.rest_account_fetch_historical_order(symbol=symbol)
            if self.fetch_historical_fill_at_start:
                await self.rest_account_fetch_historical_fill(symbol=symbol)

    async def rest_account_fetch_historical_order(self, *, symbol):
        await self.send_rest_request(rest_request_function=self.rest_account_fetch_historical_order_create_rest_request_function(symbol=symbol))

    async def rest_account_fetch_historical_fill(self, *, symbol):
        await self.send_rest_request(rest_request_function=self.rest_account_fetch_historical_fill_create_rest_request_function(symbol=symbol))

    def rest_market_data_create_get_request_function(self, **kwargs):
        def rest_request_function(*, time_point):
            rest_request = RestRequest(
                id=self.generate_next_rest_request_id(), base_url=self.rest_market_data_base_url, method=RestRequest.METHOD_GET, **kwargs
            )
            return rest_request

        return rest_request_function

    def rest_account_create_get_request_function_with_signature(self, **kwargs):
        return self.rest_account_create_request_function_with_signature(method=RestRequest.METHOD_GET, **kwargs)

    def rest_account_create_post_request_function_with_signature(self, **kwargs):
        return self.rest_account_create_request_function_with_signature(method=RestRequest.METHOD_POST, **kwargs)

    def rest_account_create_delete_request_function_with_signature(self, **kwargs):
        return self.rest_account_create_request_function_with_signature(method=RestRequest.METHOD_DELETE, **kwargs)

    def rest_account_create_request_function_with_signature(self, *, method, **kwargs):
        def rest_request_function(*, time_point):
            rest_request = RestRequest(id=self.generate_next_rest_request_id(), base_url=self.rest_account_base_url, method=method, **kwargs)
            self.sign_request(rest_request=rest_request, time_point=time_point)
            return rest_request

        return rest_request_function

    def sign_request(self, *, rest_request, time_point):
        raise NotImplementedError

    def rest_market_data_fetch_all_instrument_information_create_rest_request_function(self):
        raise NotImplementedError

    def rest_market_data_fetch_bbo_create_rest_request_function(self):
        raise NotImplementedError

    def rest_market_data_fetch_historical_trade_create_rest_request_function(self, *, symbol):
        raise NotImplementedError

    def rest_market_data_fetch_historical_ohlcv_create_rest_request_function(self, *, symbol):
        raise NotImplementedError

    def rest_account_create_order_create_rest_request_function(self, *, order):
        raise NotImplementedError

    def rest_account_cancel_order_create_rest_request_function(self, *, symbol, client_order_id):
        raise NotImplementedError

    def rest_account_fetch_order_create_rest_request_function(self, *, symbol, client_order_id):
        raise NotImplementedError

    def rest_account_fetch_open_order_create_rest_request_function(self):
        raise NotImplementedError

    def rest_account_fetch_position_create_rest_request_function(self):
        raise NotImplementedError

    def rest_account_fetch_balance_create_rest_request_function(self):
        raise NotImplementedError

    def rest_account_fetch_historical_order_create_rest_request_function(self, *, symbol):
        raise NotImplementedError

    def rest_account_fetch_historical_fill_create_rest_request_function(self, *, symbol):
        raise NotImplementedError

    def is_rest_response_success(self, *, rest_response):
        return rest_response.status_code >= 200 and rest_response.status_code < 300

    def is_rest_response_for_all_instrument_information(self, *, rest_response):
        pass

    def is_rest_response_for_bbo(self, *, rest_response):
        pass

    def is_rest_response_for_historical_trade(self, *, rest_response):
        pass

    def is_rest_response_for_historical_ohlcv(self, *, rest_response):
        pass

    def is_rest_response_for_create_order(self, *, rest_response):
        pass

    def is_rest_response_for_cancel_order(self, *, rest_response):
        pass

    def is_rest_response_for_fetch_order(self, *, rest_response):
        pass

    def is_rest_response_for_fetch_open_order(self, *, rest_response):
        pass

    def is_rest_response_for_fetch_position(self, *, rest_response):
        pass

    def is_rest_response_for_fetch_balance(self, *, rest_response):
        pass

    def is_rest_response_for_historical_order(self, *, rest_response):
        pass

    def is_rest_response_for_historical_fill(self, *, rest_response):
        pass

    def convert_rest_response_for_all_instrument_information(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_bbo(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_trade(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_trade_to_next_rest_request_function(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_ohlcv(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_ohlcv_to_next_rest_request_function(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_create_order(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_cancel_order(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_fetch_order(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_fetch_open_order(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_fetch_open_order_to_next_rest_request_function(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_fetch_position(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_fetch_balance(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_order(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_order_to_next_rest_request_function(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_fill(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    def convert_rest_response_for_historical_fill_to_next_rest_request_function(self, *, json_deserialized_payload, rest_request):
        raise NotImplementedError

    async def handle_rest_response_for_all_instrument_information(self, *, rest_response):
        all_instrument_information = self.convert_rest_response_for_all_instrument_information(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("all_instrument_information", all_instrument_information)
        ExchangeBase.logger.trace("self.all_instrument_information", all_instrument_information)
        for instrument_information in all_instrument_information:
            self.all_instrument_information[instrument_information.symbol] = instrument_information
        ExchangeBase.logger.debug("self.all_instrument_information", all_instrument_information)

    async def handle_rest_response_for_bbo(self, *, rest_response):
        bbos = self.convert_rest_response_for_bbo(json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request)
        ExchangeBase.logger.trace("bbos", bbos)
        ExchangeBase.logger.trace("self.bbos", self.bbos)
        for bbo in bbos:
            self.update_bbo(bbo=bbo)
        ExchangeBase.logger.debug("self.bbos", self.bbos)

    async def handle_rest_response_for_historical_trade(self, *, rest_response):
        historical_trades = self.convert_rest_response_for_historical_trade(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("historical_trades", historical_trades)
        ExchangeBase.logger.trace("self.trades", self.trades)
        if historical_trades:
            symbol = historical_trades[0].symbol
            historical_trades_filtered = [
                x
                for x in historical_trades
                if (
                    self.fetch_historical_trade_start_unix_timestamp_seconds is None
                    or x.exchange_update_time_point[0] >= self.fetch_historical_trade_start_unix_timestamp_seconds
                )
                and (
                    self.fetch_historical_trade_end_unix_timestamp_seconds is None
                    or x.exchange_update_time_point[0] < self.fetch_historical_trade_end_unix_timestamp_seconds
                )
            ]
            historical_trades_sorted = sorted(historical_trades_filtered, key=lambda x: (x.exchange_update_time_point, x.trade_id_as_int))
            if not self.trades.get(symbol):
                self.trades[symbol] = historical_trades_sorted
            else:
                head = self.trades[symbol][0]
                self.trades[symbol][:0] = [
                    x
                    for x in historical_trades_sorted
                    if (x.exchange_update_time_point, x.trade_id_as_int) < (head.exchange_update_time_point, head.trade_id_as_int)
                ]
        ExchangeBase.logger.debug("self.trades", self.trades)

        rest_response.next_rest_request_function = self.convert_rest_response_for_historical_trade_to_next_rest_request_function(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        rest_response.next_rest_request_delay_seconds = self.rest_market_data_send_consecutive_request_delay_seconds

        return rest_response

    async def handle_rest_response_for_historical_ohlcv(self, *, rest_response):
        historical_ohlcvs = self.convert_rest_response_for_historical_ohlcv(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("historical_ohlcvs", historical_ohlcvs)
        ExchangeBase.logger.trace("self.ohlcvs", self.ohlcvs)
        if historical_ohlcvs:
            symbol = historical_ohlcvs[0].symbol
            historical_ohlcvs_filtered = [
                x
                for x in historical_ohlcvs
                if (
                    self.fetch_historical_ohlcv_start_unix_timestamp_seconds is None
                    or x.start_unix_timestamp_seconds >= self.fetch_historical_ohlcv_start_unix_timestamp_seconds
                )
                and (
                    self.fetch_historical_ohlcv_end_unix_timestamp_seconds is None
                    or x.start_unix_timestamp_seconds < self.fetch_historical_ohlcv_end_unix_timestamp_seconds
                )
            ]
            historical_ohlcvs_sorted = sorted(historical_ohlcvs_filtered, key=lambda x: x.start_unix_timestamp_seconds)
            if not self.ohlcvs.get(symbol):
                self.ohlcvs[symbol] = historical_ohlcvs_sorted
            else:
                head = self.ohlcvs[symbol][0]
                self.ohlcvs[symbol][:0] = [x for x in historical_ohlcvs_sorted if x.start_unix_timestamp_seconds < head.start_unix_timestamp_seconds]
        ExchangeBase.logger.debug("self.ohlcvs", self.ohlcvs)

        rest_response.next_rest_request_function = self.convert_rest_response_for_historical_ohlcv_to_next_rest_request_function(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        rest_response.next_rest_request_delay_seconds = self.rest_market_data_send_consecutive_request_delay_seconds

        return rest_response

    async def handle_rest_response_for_create_order(self, *, rest_response):
        order = self.convert_rest_response_for_create_order(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("order", order)
        self.update_order(order=order)
        ExchangeBase.logger.debug("order updated", self.orders[order.symbol][order.client_order_id])

    async def handle_rest_response_for_cancel_order(self, *, rest_response):
        order = self.convert_rest_response_for_cancel_order(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("order", order)
        self.update_order(order=order)
        ExchangeBase.logger.debug("order updated", self.orders[order.symbol][order.client_order_id])

    async def handle_rest_response_for_fetch_order(self, *, rest_response):
        order = self.convert_rest_response_for_fetch_order(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("order", order)
        self.update_order(order=order)
        ExchangeBase.logger.debug("order updated", self.orders[order.symbol][order.client_order_id])

    async def handle_rest_response_for_fetch_open_order(self, *, rest_response):
        open_orders = self.convert_rest_response_for_fetch_open_order(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("open_orders", open_orders)
        ExchangeBase.logger.trace("self.orders", self.orders)
        for open_order in open_orders:
            self.update_order(order=open_order)
        ExchangeBase.logger.debug("self.orders", self.orders)

        rest_response.next_rest_request_function = self.convert_rest_response_for_fetch_open_order_to_next_rest_request_function(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        rest_response.next_rest_request_delay_seconds = self.rest_account_send_consecutive_request_delay_seconds

        return rest_response

    async def handle_rest_response_for_historical_order(self, *, rest_response):
        historical_orders = self.convert_rest_response_for_historical_order(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("historical_orders", historical_orders)
        ExchangeBase.logger.trace("self.orders", self.orders)
        for historical_order in historical_orders:
            self.update_order(order=historical_order)
        ExchangeBase.logger.trace("self.orders", self.orders)

        rest_response.next_rest_request_function = self.convert_rest_response_for_historical_order_to_next_rest_request_function(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        rest_response.next_rest_request_delay_seconds = self.rest_account_send_consecutive_request_delay_seconds

        return rest_response

    async def handle_rest_response_for_historical_fill(self, *, rest_response):
        historical_fills = self.convert_rest_response_for_historical_fill(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("historical_fills", historical_fills)
        ExchangeBase.logger.trace("self.fills", self.fills)
        if historical_fills:
            symbol = historical_fills[0].symbol
            historical_fills_filtered = [
                x
                for x in historical_fills
                if (
                    self.fetch_historical_fill_start_unix_timestamp_seconds is None
                    or x.exchange_update_time_point[0] >= self.fetch_historical_fill_start_unix_timestamp_seconds
                )
                and (
                    self.fetch_historical_fill_end_unix_timestamp_seconds is None
                    or x.exchange_update_time_point[0] < self.fetch_historical_fill_end_unix_timestamp_seconds
                )
            ]
            historical_fills_sorted = sorted(historical_fills_filtered, key=lambda x: (x.exchange_update_time_point, x.trade_id_as_int))
            if not self.fills.get(symbol):
                self.fills[symbol] = historical_fills_sorted
            else:
                head = self.fills[symbol][0]
                self.fills[symbol][:0] = [
                    x
                    for x in historical_fills_sorted
                    if (x.exchange_update_time_point, x.trade_id_as_int) < (head.exchange_update_time_point, head.trade_id_as_int)
                ]
        ExchangeBase.logger.debug("self.fills", self.fills)

        rest_response.next_rest_request_function = self.convert_rest_response_for_historical_fill_to_next_rest_request_function(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        rest_response.next_rest_request_delay_seconds = self.rest_account_send_consecutive_request_delay_seconds

        return rest_response

    async def handle_rest_response_for_fetch_position(self, *, rest_response):
        positions = self.convert_rest_response_for_fetch_position(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("positions", positions)
        ExchangeBase.logger.trace("self.positions", self.positions)
        positions_not_zero = [x for x in positions if not x.quantity_as_decimal.is_zero()]
        for position in positions_not_zero:
            self.update_position(position=position)

        self.positions = {
            symbol: positions_for_symbol for symbol, positions_for_symbol in self.positions.items() if symbol in {x.symbol for x in positions_not_zero}
        }
        ExchangeBase.logger.debug("self.positions", self.positions)

    async def handle_rest_response_for_fetch_balance(self, *, rest_response):
        balances = self.convert_rest_response_for_fetch_balance(
            json_deserialized_payload=rest_response.json_deserialized_payload, rest_request=rest_response.rest_request
        )
        ExchangeBase.logger.trace("balances", balances)
        ExchangeBase.logger.trace("self.balances", self.balances)
        balances_not_zero = [x for x in balances if not x.quantity_as_decimal.is_zero()]
        for balance in balances_not_zero:
            self.update_balance(balance=balance)

        self.balances = {
            symbol: balances_for_symbol for symbol, balances_for_symbol in self.balances.items() if symbol in {x.symbol for x in balances_not_zero}
        }
        ExchangeBase.logger.debug("self.balances", self.balances)

    async def handle_rest_response_for_error(self, *, rest_response):
        raise NotImplementedError

    async def start_websocket_connect(self, *, base_url, path, query_params):
        try:
            while True:
                url = create_url(base_url=base_url, path=path)

                websocket_connection = WebsocketConnection(base_url=base_url, path=path, query_params=query_params)
                ExchangeBase.logger.detail("websocket_connection", websocket_connection)

                try:
                    async with self.client_session.ws_connect(
                        url, params=query_params, heartbeat=self.websocket_connection_protocol_level_heartbeat_period_seconds
                    ) as client_websocket_response:
                        websocket_connection.connection = client_websocket_response

                        await self.websocket_on_connected(websocket_connection=websocket_connection)

                        raw_websocket_message = None
                        async for raw_websocket_message in websocket_connection.connection:
                            if raw_websocket_message.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    websocket_connection.latest_receive_message_time_point = time_point_now()
                                    await self.websocket_on_message(
                                        websocket_connection=websocket_connection, raw_websocket_message_data=raw_websocket_message.data
                                    )
                                except Exception as exception:
                                    ExchangeBase.logger.error(exception)

                            elif raw_websocket_message.type == aiohttp.WSMsgType.ERROR:
                                break

                        ExchangeBase.logger.warning(f"websocket connection to {websocket_connection.url_with_query_params} is closed")
                        websocket_connection_exception = websocket_connection.connection.exception()

                        if websocket_connection_exception:
                            ExchangeBase.logger.warning(repr(websocket_connection_exception))
                        else:
                            if raw_websocket_message:
                                ExchangeBase.logger.detail("last message type", raw_websocket_message.type)
                                ExchangeBase.logger.detail("last message data", raw_websocket_message.data)

                    await self.websocket_on_disconnected(websocket_connection=websocket_connection)

                except Exception as exception:
                    ExchangeBase.logger.error(exception)

                if self.websocket_connection_auto_reconnect and not self.stopped:
                    url_with_query_params = websocket_connection.url_with_query_params
                    next_websocket_reconnect_delay_seconds = self.generate_next_websocket_reconnect_delay_seconds(url_with_query_params=url_with_query_params)
                    ExchangeBase.logger.warning(
                        f"delay for {next_websocket_reconnect_delay_seconds} seconds before websocket reconnect to {url_with_query_params}"
                    )
                    await asyncio.sleep(next_websocket_reconnect_delay_seconds)
                else:
                    break

        except Exception as exception:
            ExchangeBase.logger.error(exception)

    async def send_websocket_request(self, *, websocket_connection, websocket_request):
        ExchangeBase.logger.detail("websocket_connection", websocket_connection)
        ExchangeBase.logger.detail("websocket_request", websocket_request)

        if not websocket_connection.connection.closed and websocket_request and websocket_request.payload:
            self.websocket_requests[websocket_request.id] = websocket_request
            await websocket_connection.connection.send_str(websocket_request.payload)

    async def websocket_on_message(self, *, websocket_connection, raw_websocket_message_data):
        ExchangeBase.logger.trace("raw_websocket_message_data", raw_websocket_message_data)

        websocket_message = WebsocketMessage(
            websocket_connection=websocket_connection, payload=raw_websocket_message_data, json_deserialize=self.json_deserialize
        )
        websocket_message = self.websocket_on_message_extract_data(websocket_message=websocket_message)
        websocket_request = None
        if websocket_message.websocket_request_id:
            websocket_request = self.websocket_requests.pop(websocket_message.websocket_request_id, None)
            websocket_message.websocket_request = websocket_request
        ExchangeBase.logger.detail("websocket_message", websocket_message)

        if self.is_websocket_push_data(websocket_message=websocket_message):
            if self.is_websocket_push_data_for_bbo(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_bbo(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_trade(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_trade(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_ohlcv(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_ohlcv(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_order(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_order(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_fill(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_fill(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_position(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_position(websocket_message=websocket_message)

            elif self.is_websocket_push_data_for_balance(websocket_message=websocket_message):
                await self.handle_websocket_push_data_for_balance(websocket_message=websocket_message)

        elif self.is_websocket_response_success(websocket_message=websocket_message):
            if self.is_websocket_response_for_create_order(websocket_message=websocket_message):
                await self.handle_websocket_response_for_create_order(websocket_message=websocket_message)

            elif self.is_websocket_response_for_cancel_order(websocket_message=websocket_message):
                await self.handle_websocket_response_for_cancel_order(websocket_message=websocket_message)

            elif self.is_websocket_response_for_subscribe(websocket_message=websocket_message):
                await self.handle_websocket_response_for_subscribe(websocket_message=websocket_message)

            elif self.is_websocket_response_for_login(websocket_message=websocket_message):
                await self.handle_websocket_response_for_login(websocket_message=websocket_message)

        else:
            await self.handle_websocket_response_for_error(websocket_message=websocket_message)

    @property
    def websocket_account_trade_url_with_query_params(self):
        return create_url_with_query_params(
            base_url=self.websocket_account_trade_base_url, path=self.websocket_account_trade_path, query_params=self.websocket_account_trade_query_params
        )

    async def websocket_login(self, *, websocket_connection):
        await self.send_websocket_request(
            websocket_connection=websocket_connection, websocket_request=self.websocket_login_create_websocket_request(time_point=time_point_now())
        )

    async def websocket_market_data_connect(self):
        if self.symbols and (self.subscribe_bbo or self.subscribe_trade or self.subscribe_ohlcv):
            self.all_tasks.append(
                asyncio.create_task(
                    self.start_websocket_connect(
                        base_url=self.websocket_market_data_base_url, path=self.websocket_market_data_path, query_params=self.websocket_market_data_query_params
                    )
                )
            )

    async def websocket_market_data_subscribe(self, *, websocket_connection):
        symbols_subsets = convert_set_to_subsets(input=self.symbols, subset_length=self.websocket_market_data_channel_symbols_limit)
        for symbols_subset in symbols_subsets:
            await self.send_websocket_request(
                websocket_connection=websocket_connection,
                websocket_request=self.websocket_market_data_update_subscribe_create_websocket_request(symbols=symbols_subset, is_subscribe=True),
            )
            if self.websocket_market_data_channel_send_consecutive_request_delay_seconds:
                await asyncio.sleep(self.websocket_market_data_channel_send_consecutive_request_delay_seconds)

    async def websocket_account_connect(self):
        if self.subscribe_order or self.subscribe_fill or self.subscribe_position or self.subscribe_balance:
            self.all_tasks.append(
                asyncio.create_task(
                    self.start_websocket_connect(
                        base_url=self.websocket_account_base_url, path=self.websocket_account_path, query_params=self.websocket_account_query_params
                    )
                )
            )

    async def websocket_account_subscribe(self, *, websocket_connection):
        await self.send_websocket_request(
            websocket_connection=websocket_connection, websocket_request=self.websocket_account_update_subscribe_create_websocket_request(is_subscribe=True)
        )

    async def websocket_account_create_order(self, *, websocket_connection, order):
        try:
            order_to_create = self.create_order_ensure_client_order_id(order=order)
            await self.send_websocket_request(
                websocket_connection=websocket_connection, websocket_request=self.websocket_account_create_order_create_websocket_request(order=order_to_create)
            )
            return order_to_create
        except Exception as exception:
            ExchangeBase.logger.error(exception)

    async def websocket_account_cancel_order(self, *, websocket_connection, symbol, client_order_id):
        try:
            await self.send_websocket_request(
                websocket_connection=websocket_connection,
                websocket_request=self.websocket_account_cancel_order_create_websocket_request(symbol=symbol, client_order_id=client_order_id),
            )
        except Exception as exception:
            ExchangeBase.logger.error(exception)

    def websocket_create_request(self, **kwargs):
        if "id" in kwargs:
            websocket_request = WebsocketRequest(**kwargs)
        else:
            websocket_request = WebsocketRequest(id=self.generate_next_websocket_request_id(), **kwargs)

        return websocket_request

    def websocket_connection_ping_on_application_level_create_websocket_request(self):
        raise NotImplementedError

    def websocket_login_create_websocket_request(self, *, time_point):
        raise NotImplementedError

    def websocket_market_data_update_subscribe_create_websocket_request(self, *, symbols, is_subscribe):
        raise NotImplementedError

    def websocket_account_update_subscribe_create_websocket_request(self, *, is_subscribe):
        raise NotImplementedError

    def websocket_account_create_order_create_websocket_request(self, *, order):
        raise NotImplementedError

    def websocket_account_cancel_order_create_websocket_request(self, *, symbol, client_order_id):
        raise NotImplementedError

    async def websocket_on_connected(self, *, websocket_connection):
        ExchangeBase.logger.trace("websocket_connection", websocket_connection)
        self.websocket_connections[websocket_connection.url_with_query_params] = websocket_connection
        await self.handle_websocket_on_connected(websocket_connection=websocket_connection)

    async def handle_websocket_on_connected(self, *, websocket_connection):
        if websocket_connection.path == self.websocket_market_data_path:
            await self.websocket_market_data_subscribe(websocket_connection=websocket_connection)
        elif websocket_connection.path == self.websocket_account_path:
            await self.websocket_login(websocket_connection=websocket_connection)

    async def websocket_on_disconnected(self, *, websocket_connection):
        ExchangeBase.logger.trace("websocket_connection", websocket_connection)
        await self.handle_websocket_on_disconnected(websocket_connection=websocket_connection)
        self.websocket_connections.pop(websocket_connection.url_with_query_params, None)
        self.websocket_logged_in_connections.discard(websocket_connection.url_with_query_params)

    async def handle_websocket_on_disconnected(self, *, websocket_connection):
        pass

    def websocket_on_message_extract_data(self, *, websocket_message):
        raise NotImplementedError

    def is_websocket_push_data(self, *, websocket_message):
        return websocket_message.websocket_request_id is None

    def is_websocket_push_data_for_bbo(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_trade(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_ohlcv(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_order(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_fill(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_position(self, *, websocket_message):
        pass

    def is_websocket_push_data_for_balance(self, *, websocket_message):
        pass

    def is_websocket_response_success(self, *, websocket_message):
        pass

    def is_websocket_response_for_create_order(self, *, websocket_message):
        pass

    def is_websocket_response_for_cancel_order(self, *, websocket_message):
        pass

    def is_websocket_response_for_subscribe(self, *, websocket_message):
        pass

    def is_websocket_response_for_login(self, *, websocket_message):
        pass

    def convert_websocket_push_data_for_bbo(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_trade(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_ohlcv(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_order(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_fill(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_position(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_push_data_for_balance(self, *, json_deserialized_payload):
        raise NotImplementedError

    def convert_websocket_response_for_create_order(self, *, json_deserialized_payload, websocket_request):
        raise NotImplementedError

    def convert_websocket_response_for_cancel_order(self, *, json_deserialized_payload, websocket_request):
        raise NotImplementedError

    async def handle_websocket_push_data_for_bbo(self, *, websocket_message):
        bbos = self.convert_websocket_push_data_for_bbo(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("bbos", bbos)
        ExchangeBase.logger.trace("self.bbos", self.bbos)
        for bbo in bbos:
            self.update_bbo(bbo=bbo)
        ExchangeBase.logger.debug("self.bbos", self.bbos)

    async def handle_websocket_push_data_for_trade(self, *, websocket_message):
        trades = self.convert_websocket_push_data_for_trade(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("trades", trades)
        ExchangeBase.logger.trace("self.trades", self.trades)
        if trades:
            symbol = trades[0].symbol
            trades_sorted = sorted(trades, key=lambda x: (x.exchange_update_time_point, x.trade_id_as_int))
            if not self.trades.get(symbol):
                self.trades[symbol] = trades_sorted
            else:
                tail = self.trades[symbol][-1]
                self.trades[symbol].extend(
                    [x for x in trades_sorted if (x.exchange_update_time_point, x.trade_id_as_int) > (tail.exchange_update_time_point, tail.trade_id_as_int)]
                )
        ExchangeBase.logger.debug("self.trades", self.trades)

    async def handle_websocket_push_data_for_ohlcv(self, *, websocket_message):
        ohlcvs = self.convert_websocket_push_data_for_ohlcv(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("ohlcvs", ohlcvs)
        ExchangeBase.logger.trace("self.ohlcvs", self.ohlcvs)
        if ohlcvs:
            symbol = ohlcvs[0].symbol
            ohlcvs_sorted = sorted(ohlcvs, key=lambda x: x.start_unix_timestamp_seconds)
            if not self.ohlcvs.get(symbol):
                self.ohlcvs[symbol] = ohlcvs_sorted
            else:
                tail = self.ohlcvs[symbol][-1]
                if tail.start_unix_timestamp_seconds == ohlcvs_sorted[0].start_unix_timestamp_seconds:
                    self.ohlcvs[symbol][-1] = ohlcvs_sorted[0]
                self.ohlcvs[symbol].extend([x for x in ohlcvs_sorted if (x.start_unix_timestamp_seconds) > (tail.start_unix_timestamp_seconds)])
        ExchangeBase.logger.debug("self.ohlcvs", self.ohlcvs)

    async def handle_websocket_push_data_for_order(self, *, websocket_message):
        orders = self.convert_websocket_push_data_for_order(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("orders", orders)
        ExchangeBase.logger.trace("self.orders", self.orders)
        for order in orders:
            self.update_order(order=order)
        ExchangeBase.logger.debug("self.orders", self.orders)

    async def handle_websocket_push_data_for_fill(self, *, websocket_message):
        fills = self.convert_websocket_push_data_for_fill(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("fills", fills)
        ExchangeBase.logger.trace("self.fills", self.fills)
        if fills:
            symbol = fills[0].symbol
            fills_sorted = sorted(fills, key=lambda x: (x.exchange_update_time_point, x.trade_id_as_int))
            if not self.fills.get(symbol):
                self.fills[symbol] = fills_sorted
            else:
                tail = self.fills[symbol][-1]
                self.fills[symbol].extend(
                    [x for x in fills_sorted if (x.exchange_update_time_point, x.trade_id_as_int) > (tail.exchange_update_time_point, tail.trade_id_as_int)]
                )
        ExchangeBase.logger.debug("self.fills", self.fills)

    async def handle_websocket_push_data_for_position(self, *, websocket_message):
        positions = self.convert_websocket_push_data_for_position(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("positions", positions)
        ExchangeBase.logger.trace("self.positions", self.positions)
        for position in positions:
            self.update_position(position=position)
        ExchangeBase.logger.debug("self.positions", self.positions)

    async def handle_websocket_push_data_for_balance(self, *, websocket_message):
        balances = self.convert_websocket_push_data_for_balance(json_deserialized_payload=websocket_message.json_deserialized_payload)
        ExchangeBase.logger.trace("balances", balances)
        ExchangeBase.logger.trace("self.balances", self.balances)
        for balance in balances:
            self.update_balance(balance=balance)
        ExchangeBase.logger.debug("self.balances", self.balances)

    async def handle_websocket_response_for_create_order(self, *, websocket_message):
        order = self.convert_websocket_response_for_create_order(
            json_deserialized_payload=websocket_message.json_deserialized_payload, websocket_request=websocket_message.websocket_request
        )
        ExchangeBase.logger.trace("order", order)
        self.update_order(order=order)
        ExchangeBase.logger.debug("order updated", self.orders[order.symbol][order.client_order_id])

    async def handle_websocket_response_for_cancel_order(self, *, websocket_message):
        order = self.convert_websocket_response_for_cancel_order(
            json_deserialized_payload=websocket_message.json_deserialized_payload, websocket_request=websocket_message.websocket_request
        )
        ExchangeBase.logger.trace("order", order)
        self.update_order(order=order)
        ExchangeBase.logger.debug("order updated", self.orders[order.symbol][order.client_order_id])

    async def handle_websocket_response_for_subscribe(self, *, websocket_message):
        ExchangeBase.logger.info("websocket_message", websocket_message)
        websocket_connection = websocket_message.websocket_connection
        self.reset_websocket_reconnect_delay(url_with_query_params=websocket_connection.url_with_query_params)

    async def handle_websocket_response_for_login(self, *, websocket_message):
        ExchangeBase.logger.info("websocket_message", websocket_message)
        websocket_connection = websocket_message.websocket_connection
        url_with_query_params = websocket_connection.url_with_query_params
        self.websocket_logged_in_connections.add(url_with_query_params)
        self.reset_websocket_reconnect_delay(url_with_query_params=websocket_connection.url_with_query_params)
        if websocket_connection.path == self.websocket_account_path:
            await self.websocket_account_subscribe(websocket_connection=websocket_connection)

    def handle_websocket_response_for_error(self, *, websocket_message):
        raise NotImplementedError

    def reset_websocket_reconnect_delay(self, *, url_with_query_params):
        async def start_reset_websocket_reconnect_delay():
            try:
                await asyncio.sleep(self.reset_websocket_reconnect_delay_delay_seconds)
                self.websocket_reconnect_delay_seconds.pop(url_with_query_params, None)
            except Exception as exception:
                ExchangeBase.logger.error(exception)

        self.all_tasks.append(asyncio.create_task(start_reset_websocket_reconnect_delay()))

    def generate_next_websocket_reconnect_delay_seconds(self, *, url_with_query_params):
        if url_with_query_params not in self.websocket_reconnect_delay_seconds:
            self.websocket_reconnect_delay_seconds[url_with_query_params] = self.websocket_reconnect_delay_seconds_exponential_backoff_initial
        else:
            self.websocket_reconnect_delay_seconds[url_with_query_params] = min(
                self.websocket_reconnect_delay_seconds[url_with_query_params] * self.websocket_reconnect_delay_seconds_exponential_backoff_base,
                self.websocket_reconnect_delay_seconds_exponential_backoff_max,
            )
        return self.websocket_reconnect_delay_seconds[url_with_query_params]

    def update_bbo(self, *, bbo):
        if bbo.symbol not in self.bbos or (
            self.bbos[bbo.symbol].exchange_update_time_point is None
            or bbo.exchange_update_time_point is None
            or self.bbos[bbo.symbol].exchange_update_time_point < bbo.exchange_update_time_point
        ):
            self.bbos[bbo.symbol] = bbo

    def has_order(self, *, symbol, client_order_id):
        return symbol in self.orders and client_order_id in self.orders[symbol]

    def get_order(self, *, symbol, client_order_id):
        return self.orders.get(symbol, {}).get(client_order_id)

    def upsert_order(self, *, order):
        if order.symbol not in self.orders:
            self.orders[order.symbol] = {}
        self.orders[order.symbol][order.client_order_id] = order

    def replace_order(self, *, symbol, client_order_id, **kwargs):
        if self.has_order(symbol=symbol, client_order_id=client_order_id):
            self.orders[symbol][client_order_id] = dataclasses.replace(self.orders[symbol][client_order_id], **kwargs)

    def update_order(self, *, order):
        order_to_update = self.get_order(symbol=order.symbol, client_order_id=order.client_order_id)

        if order_to_update:
            exchange_update_time_point = order_to_update.exchange_update_time_point
            status = order_to_update.status
            cumulative_filled_quantity = order_to_update.cumulative_filled_quantity
            has_fill = order.cumulative_filled_quantity is not None and (
                cumulative_filled_quantity is None or order.cumulative_filled_quantity_as_decimal > Decimal(cumulative_filled_quantity)
            )

            if (
                (
                    order.exchange_update_time_point is not None
                    and (exchange_update_time_point is None or order.exchange_update_time_point > exchange_update_time_point)
                )
                or (order.status is not None and (status is None or order.status > status))
                or has_fill
            ):
                api_method = order_to_update.api_method
                symbol = order_to_update.symbol
                exchange_update_time_point = order.exchange_update_time_point
                order_id = order_to_update.order_id

                if order.order_id is not None and order.order_id != order_id:
                    order_id = order.order_id

                client_order_id = order_to_update.client_order_id
                is_buy = order_to_update.is_buy

                price = order_to_update.price
                if order.price is not None and order.price != price:
                    price = order.price

                quantity = order_to_update.quantity
                if order.quantity is not None and order.quantity != quantity:
                    quantity = order.quantity

                is_post_only = order_to_update.is_post_only
                is_fok = order_to_update.is_fok
                is_ioc = order_to_update.is_ioc
                is_reduce_only = order_to_update.is_reduce_only

                cumulative_filled_quantity = order_to_update.cumulative_filled_quantity
                cumulative_filled_quote_quantity = order_to_update.cumulative_filled_quote_quantity
                if has_fill:
                    cumulative_filled_quantity = order.cumulative_filled_quantity
                    cumulative_filled_quote_quantity = order.cumulative_filled_quote_quantity

                exchange_create_time_point = order_to_update.exchange_create_time_point
                if exchange_create_time_point is None and order.exchange_create_time_point is not None:
                    exchange_create_time_point = order.exchange_create_time_point

                status = order.status

                self.upsert_order(
                    order=Order(
                        api_method=api_method,
                        symbol=symbol,
                        exchange_update_time_point=exchange_update_time_point,
                        order_id=order_id,
                        client_order_id=client_order_id,
                        is_buy=is_buy,
                        price=price,
                        quantity=quantity,
                        is_post_only=is_post_only,
                        is_fok=is_fok,
                        is_ioc=is_ioc,
                        is_reduce_only=is_reduce_only,
                        cumulative_filled_quantity=cumulative_filled_quantity,
                        cumulative_filled_quote_quantity=cumulative_filled_quote_quantity,
                        exchange_create_time_point=exchange_create_time_point,
                        status=status,
                    )
                )
        else:
            self.upsert_order(order=order)

    def update_position(self, *, position):
        if position.symbol not in self.positions or (
            self.positions[position.symbol].exchange_update_time_point is None
            or position.exchange_update_time_point is None
            or self.positions[position.symbol].exchange_update_time_point < position.exchange_update_time_point
        ):
            if position.quantity_as_decimal.is_zero():
                self.positions.pop(position.symbol, None)
            else:
                self.positions[position.symbol] = position

    def update_balance(self, *, balance):
        if balance.symbol not in self.balances or (
            self.balances[balance.symbol].exchange_update_time_point is None
            or balance.exchange_update_time_point is None
            or self.balances[balance.symbol].exchange_update_time_point < balance.exchange_update_time_point
        ):
            if balance.quantity_as_decimal.is_zero():
                self.balances.pop(balance.symbol, None)
            else:
                self.balances[balance.symbol] = balance

    def prune_trades(self):
        ExchangeBase.logger.trace("self.trades", self.trades)

        if self.keep_historical_trade_seconds:
            for symbol, trades_for_symbol in self.trades.items():
                if trades_for_symbol:
                    head_exchange_update_time_point = trades_for_symbol[0].exchange_update_time_point[0]
                    earliest_exchange_update_time_point_to_keep = trades_for_symbol[-1].exchange_update_time_point[0] - self.keep_historical_trade_seconds

                    if head_exchange_update_time_point < earliest_exchange_update_time_point_to_keep:
                        self.trades[symbol] = [x for x in trades_for_symbol if x.exchange_update_time_point[0] >= earliest_exchange_update_time_point_to_keep]

        ExchangeBase.logger.debug("self.trades", self.trades)

    def prune_ohlcvs(self):
        ExchangeBase.logger.trace("self.ohlcvs", self.ohlcvs)

        if self.keep_historical_ohlcv_seconds:
            for symbol, ohlcvs_for_symbol in self.ohlcvs.items():
                head_start_unix_timestamp_seconds = ohlcvs_for_symbol[0].start_unix_timestamp_seconds
                earliest_start_unix_timestamp_seconds_to_keep = ohlcvs_for_symbol[-1].start_unix_timestamp_seconds - self.keep_historical_ohlcv_seconds

                if head_start_unix_timestamp_seconds < earliest_start_unix_timestamp_seconds_to_keep:
                    self.ohlcvs[symbol] = [x for x in ohlcvs_for_symbol if x.start_unix_timestamp_seconds >= earliest_start_unix_timestamp_seconds_to_keep]

        ExchangeBase.logger.debug("self.ohlcvs", self.ohlcvs)

    def prune_orders(self):
        ExchangeBase.logger.trace("self.orders", self.orders)

        if self.keep_historical_order_seconds:
            for symbol, orders_for_symbol in self.orders.items():
                latest_exchange_update_time_point = None
                for order in orders_for_symbol.values():
                    if (
                        order.is_closed
                        and order.exchange_update_time_point is not None
                        and (latest_exchange_update_time_point is None or order.exchange_update_time_point > latest_exchange_update_time_point)
                    ):
                        latest_exchange_update_time_point = order.exchange_update_time_point

                if latest_exchange_update_time_point is not None:
                    earliest_exchange_update_time_point_to_keep = latest_exchange_update_time_point[0] - self.keep_historical_order_seconds
                    self.orders[symbol] = {
                        client_order_id: order
                        for client_order_id, order in self.orders[symbol].items()
                        if not order.is_closed
                        or (order.exchange_update_time_point is not None and order.exchange_update_time_point[0] >= earliest_exchange_update_time_point_to_keep)
                    }

        ExchangeBase.logger.debug("self.orders", self.orders)

    def prune_fills(self):
        ExchangeBase.logger.trace("self.fills", self.fills)

        if self.keep_historical_fill_seconds:
            for symbol, fills_for_symbol in self.fills.items():
                if fills_for_symbol:
                    head_exchange_update_time_point = fills_for_symbol[0].exchange_update_time_point[0]
                    earliest_exchange_update_time_point_to_keep = fills_for_symbol[-1].exchange_update_time_point[0] - self.keep_historical_fill_seconds

                    if head_exchange_update_time_point < earliest_exchange_update_time_point_to_keep:
                        self.fills[symbol] = [x for x in fills_for_symbol if x.exchange_update_time_point[0] >= earliest_exchange_update_time_point_to_keep]

        ExchangeBase.logger.debug("self.fills", self.fills)

    def generate_next_rest_request_id(self):
        self.next_rest_request_id_int += 1
        return str(self.next_rest_request_id_int)

    def generate_next_websocket_request_id(self):
        self.next_websocket_request_id_int += 1
        return str(self.next_websocket_request_id_int)

    def generate_next_client_order_id(self):
        unix_timestamp_milliseconds = unix_timestamp_milliseconds_now()

        if self.last_client_order_id_unix_timestamp_milliseconds != unix_timestamp_milliseconds:
            self.last_client_order_id_unix_timestamp_milliseconds = unix_timestamp_milliseconds
            self.last_client_order_id_sequence_number = 0
        else:
            self.last_client_order_id_sequence_number += 1

        return f"{self.last_client_order_id_unix_timestamp_milliseconds}{str(self.last_client_order_id_sequence_number).zfill(3)}"
