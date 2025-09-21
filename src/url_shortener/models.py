from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class ShortUrl:
    code: str
    target: str
    created_at: datetime
    hits: int = 0
    expires_at: Optional[datetime] = None

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        n = now or datetime.utcnow()
        return self.expires_at is not None and n >= self.expires_at

    def with_incremented_hits(self) -> "ShortUrl":
        return ShortUrl(
            code=self.code,
            target=self.target,
            created_at=self.created_at,
            hits=self.hits + 1,
            expires_at=self.expires_at,
        )
