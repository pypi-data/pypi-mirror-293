from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True, kw_only=True)
class ModelBase:
    api_method: Optional[str] = None
    symbol: Optional[str] = None
    exchange_update_time_point: Optional[Tuple[int, int]] = None
