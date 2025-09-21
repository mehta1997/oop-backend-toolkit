import time
from datetime import timedelta

# URL Shortener imports
from src.url_shortener.repositories import InMemoryShortUrlRepository
from src.url_shortener.services import ShortenerService, CreateShortUrlRequest

# Rate Limiter import
from src.rate_limiter.token_bucket import TokenBucket

# LRU Cache import
from src.cache.lru_cache import LRUCache


def demo_url_shortener():
    print("\n=== URL SHORTENER DEMO ===")
    repo = InMemoryShortUrlRepository()
    svc = ShortenerService(repo)

    print("Creating short URL for https://example.com (TTL 3s)...")
    s = svc.create(CreateShortUrlRequest(target="https://example.com", ttl_seconds=3))
    print(f" Short code: {s.code}")
    print(" Resolving immediately ->", svc.resolve(s.code))

    print(" Waiting 4 seconds so it expires...")
    time.sleep(4)
    print(" Resolving after expiry ->", svc.resolve(s.code))  # should be None
    print("All records in repo:", list(repo.all()))


def demo_rate_limiter():
    print("\n=== TOKEN-BUCKET RATE LIMITER DEMO ===")
    bucket = TokenBucket(capacity=2.0, refill_rate_per_sec=1.0)
    print("Bucket capacity=2, refill=1 token/sec")
    for i in range(5):
        ok = bucket.try_consume()
        print(f" Request {i+1}: {'ALLOWED' if ok else 'BLOCKED'} (tokens ~ {bucket.tokens:.2f})")
        if not ok:
            print("  Sleeping 1.2s to allow refill...")
            time.sleep(1.2)


def demo_lru_cache():
    print("\n=== LRU CACHE DEMO ===")
    cache = LRUCache[int, str](capacity=2)
    print("Capacity = 2")
    cache.put(1, "A"); print(" put(1,'A')")
    cache.put(2, "B"); print(" put(2,'B')")
    print(" get(1) ->", cache.get(1), "(1 becomes MRU)")
    cache.put(3, "C"); print(" put(3,'C')  # evicts key 2 (LRU)")
    print(" get(2) ->", cache.get(2))  # None
    print(" get(1) ->", cache.get(1))
    print(" get(3) ->", cache.get(3))


if __name__ == "__main__":
    demo_url_shortener()
    demo_rate_limiter()
    demo_lru_cache()
    print("\nDONE.")
