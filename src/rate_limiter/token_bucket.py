from __future__ import annotations
from dataclasses import dataclass
from time import monotonic


@dataclass
class TokenBucket:
    capacity: float
    refill_rate_per_sec: float
    _tokens: float = 0.0
    _last: float = 0.0

    def __post_init__(self) -> None:
        self._tokens = self.capacity
        self._last = monotonic()

    def _refill(self) -> None:
        now = monotonic()
        elapsed = max(0.0, now - self._last)
        self._last = now
        self._tokens = min(self.capacity, self._tokens + self.refill_rate_per_sec * elapsed)

    def try_consume(self, tokens: float = 1.0) -> bool:
        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    @property
    def tokens(self) -> float:
        self._refill()
        return self._tokens
