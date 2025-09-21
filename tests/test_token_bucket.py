import time
from src.rate_limiter.token_bucket import TokenBucket

def test_token_bucket_refills_and_limits():
    bucket = TokenBucket(capacity=2.0, refill_rate_per_sec=1.0)
    assert bucket.try_consume() is True
    assert bucket.try_consume() is True
    # now empty
    assert bucket.try_consume() is False
    time.sleep(1.2)
    assert bucket.try_consume() is True
