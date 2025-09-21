from datetime import datetime, timedelta
from src.url_shortener.repositories import InMemoryShortUrlRepository
from src.url_shortener.services import ShortenerService, CreateShortUrlRequest

def test_create_and_resolve_roundtrip():
    repo = InMemoryShortUrlRepository()
    svc = ShortenerService(repo)
    s = svc.create(CreateShortUrlRequest(target="https://example.com", ttl_seconds=10))
    assert repo.exists(s.code)
    resolved = svc.resolve(s.code)
    assert resolved == "https://example.com"

def test_expiry():
    repo = InMemoryShortUrlRepository()
    svc = ShortenerService(repo)
    s = svc.create(CreateShortUrlRequest(target="https://x", ttl_seconds=1))
    # simulate time passed by injecting a 'now' beyond expiry
    future = s.created_at + timedelta(seconds=120)
    assert svc.resolve(s.code, now=future) is None
