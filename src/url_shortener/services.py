from __future__ import annotations
import hashlib
import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from .interfaces import ShortUrlRepository
from .models import ShortUrl


def _safe_code_from(target: str, length: int = 7) -> str:
    # deterministic fallback, used only if we choose to hash
    digest = hashlib.sha256(target.encode()).hexdigest()
    return digest[:length]


@dataclass
class CreateShortUrlRequest:
    target: str
    ttl_seconds: Optional[int] = None
    custom_code: Optional[str] = None


class ShortenerService:
    """Business logic layer; depends on an abstract repository."""
    def __init__(self, repo: ShortUrlRepository) -> None:
        self.repo = repo

    def _random_code(self, length: int = 7) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(random.choice(alphabet) for _ in range(length))

    def create(self, req: CreateShortUrlRequest) -> ShortUrl:
        code = req.custom_code or self._random_code()
        # avoid collisions; very small loop expected for demo
        attempts = 0
        while self.repo.exists(code):
            attempts += 1
            if attempts > 3:  # fall back to deterministic+salt path on too many collisions
                code = _safe_code_from(req.target + str(attempts))
                break
            code = self._random_code()

        expires_at = None
        if req.ttl_seconds:
            expires_at = datetime.utcnow() + timedelta(seconds=req.ttl_seconds)

        s = ShortUrl(code=code, target=req.target, created_at=datetime.utcnow(), expires_at=expires_at)
        self.repo.save(s)
        return s

    def resolve(self, code: str, now: Optional[datetime] = None) -> Optional[str]:
        record = self.repo.get(code)
        if not record:
            return None
        if record.is_expired(now):
            return None
        # increment hits immutably
        updated = record.with_incremented_hits()
        self.repo.save(updated)
        return updated.target
