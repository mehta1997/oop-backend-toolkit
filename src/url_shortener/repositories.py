from __future__ import annotations
import json
from typing import Dict, Iterable, Optional
from datetime import datetime
from .interfaces import ShortUrlRepository
from .models import ShortUrl


class InMemoryShortUrlRepository(ShortUrlRepository):
    def __init__(self) -> None:
        self._data: Dict[str, ShortUrl] = {}

    def get(self, code: str) -> Optional[ShortUrl]:
        return self._data.get(code)

    def save(self, item: ShortUrl) -> None:
        self._data[item.code] = item

    def exists(self, code: str) -> bool:
        return code in self._data

    def all(self) -> Iterable[ShortUrl]:
        return list(self._data.values())


class JsonFileShortUrlRepository(ShortUrlRepository):
    """Tiny file-backed repo for demo purposes (not concurrent-safe)."""
    def __init__(self, path: str) -> None:
        self.path = path
        try:
            with open(self.path, "r") as f:
                self._raw = json.load(f)
        except FileNotFoundError:
            self._raw = {}
            self._flush()

    def _flush(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self._raw, f)

    def _to_model(self, code: str, payload) -> ShortUrl:
        return ShortUrl(
            code=code,
            target=payload["target"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            hits=payload["hits"],
            expires_at=datetime.fromisoformat(payload["expires_at"]) if payload["expires_at"] else None,
        )

    def _to_payload(self, s: ShortUrl):
        return {
            "target": s.target,
            "created_at": s.created_at.isoformat(),
            "hits": s.hits,
            "expires_at": s.expires_at.isoformat() if s.expires_at else None,
        }

    def get(self, code: str) -> Optional[ShortUrl]:
        p = self._raw.get(code)
        return self._to_model(code, p) if p else None

    def save(self, item: ShortUrl) -> None:
        self._raw[item.code] = self._to_payload(item)
        self._flush()

    def exists(self, code: str) -> bool:
        return code in self._raw

    def all(self) -> Iterable[ShortUrl]:
        return [self._to_model(c, p) for c, p in self._raw.items()]
