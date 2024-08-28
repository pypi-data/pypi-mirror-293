import os
import pprint
import sys
import traceback
from datetime import datetime, timezone
from inspect import getframeinfo, stack

from crypto_chassis_trade.core.network.rest_request import RestRequest
from crypto_chassis_trade.core.network.rest_response import RestResponse
from crypto_chassis_trade.core.network.websocket_connection import WebsocketConnection
from crypto_chassis_trade.core.network.websocket_message import WebsocketMessage
from crypto_chassis_trade.core.network.websocket_request import WebsocketRequest
from crypto_chassis_trade.utility.logger_interface import LoggerInterface, LogLevel


class Logger(LoggerInterface):
    def __init__(self, *, name="", level=LogLevel.WARNING):
        self.name = name
        self.level = level
        self.message_format = "{} {} {{{}:{}:{}}} {}"
        self.separator = "\n"

    def pretty_format(self, object, width=160):
        if (
            isinstance(object, RestRequest)
            or isinstance(object, RestResponse)
            or isinstance(object, WebsocketConnection)
            or isinstance(object, WebsocketMessage)
            or isinstance(object, WebsocketRequest)
        ):
            return pprint.pformat(object.as_pretty_dict(), width=width)
        else:
            return pprint.pformat(object, width=width)

    def trace(self, *messages: str) -> None:
        if self.level <= LogLevel.TRACE:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{self.separator.join((self.pretty_format(x) for x in messages))}\n",
                )
            )

    def debug(self, *messages: str) -> None:
        if self.level <= LogLevel.DEBUG:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{self.separator.join((self.pretty_format(x) for x in messages))}\n",
                )
            )

    def detail(self, *messages: str) -> None:
        if self.level <= LogLevel.DETAIL:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{self.separator.join((self.pretty_format(x) for x in messages))}\n",
                )
            )

    def info(self, *messages: str) -> None:
        if self.level <= LogLevel.INFO:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{self.separator.join((self.pretty_format(x) for x in messages))}\n",
                )
            )

    def warning(self, *messages: str) -> None:
        if self.level <= LogLevel.WARNING:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{self.separator.join((self.pretty_format(x) for x in messages))}\n",
                )
            )

    def error(self, exception: Exception) -> None:
        if self.level <= LogLevel.ERROR:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{repr(exception)}{10*' '}{traceback.format_exc()}\n",
                )
            )
            if os.environ.get("CRYPTO_CHASSIS_TRADE_TEST_FLAG"):
                sys.exit(1)

    def critical(self, exception: Exception) -> None:
        if self.level <= LogLevel.CRITICAL:
            this_function = getframeinfo(stack()[0][0])
            caller = getframeinfo(stack()[1][0])
            print(
                self.message_format.format(
                    datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    self.name,
                    os.path.basename(caller.filename),
                    caller.function,
                    caller.lineno,
                    f"{this_function.function.upper()}{10*' '}{repr(exception)}{10*' '}{traceback.format_exc()}\n",
                )
            )
            sys.exit(1)
