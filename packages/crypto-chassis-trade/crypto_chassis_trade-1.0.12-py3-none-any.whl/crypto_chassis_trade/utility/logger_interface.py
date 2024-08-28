from enum import IntEnum


class LogLevel(IntEnum):
    TRACE = 1
    DEBUG = 2
    DETAIL = 3
    INFO = 4
    WARNING = 5
    ERROR = 6
    CRITICAL = 7
    NONE = 8


class LoggerInterface:

    def trace(self, *messages: str) -> None:
        raise NotImplementedError

    def debug(self, *messages: str) -> None:
        raise NotImplementedError

    def detail(self, *messages: str) -> None:
        raise NotImplementedError

    def info(self, *messages: str) -> None:
        raise NotImplementedError

    def warning(self, *messages: str) -> None:
        raise NotImplementedError

    def error(self, exception: Exception) -> None:
        raise NotImplementedError

    def critical(self, exception: Exception) -> None:
        raise NotImplementedError
