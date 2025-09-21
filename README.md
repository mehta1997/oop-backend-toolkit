````markdown
# OOP Backend Toolkit

A small collection of Python components demonstrating object-oriented design patterns:
- A URL shortener with TTL support
- An LRU cache
- A token bucket rate limiter

All components are written in plain Python with minimal dependencies and come with simple demos and tests.

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Run the live demo
python live_demo.py

# Run FastAPI app (serves URL shortener endpoints)
uvicorn app_fastapi:app --reload
````

## Project Layout

```
├── app_fastapi.py            # FastAPI entrypoint for URL shortener
├── demo.py                   # Minimal CLI demo
├── live_demo.py              # Combined demo for all components
├── src/
│   ├── cache/
│   │   ├── lru_cache.py      # Linked-list/dict LRU cache
│   │   └── lru.py            # OrderedDict-based LRU cache
│   ├── rate_limiter/
│   │   └── token_bucket.py   # Token bucket implementation
│   └── url_shortener/
│       ├── interfaces.py     # Repository interface
│       ├── models.py         # ShortUrl model
│       ├── repositories.py   # In-memory + JSON repositories
│       └── services.py       # Shortener service layer
├── tests/                    # Pytest test suite
├── README.md
├── requirements.txt
├── pyproject.toml
└── LICENSE
```

## Design Notes

This project is built around a few small but reusable building blocks, each chosen for clarity and predictable performance:

* **URL Shortener**
  The shortener uses a repository + service pattern. The repository isolates storage (in-memory or JSON file) so it can be swapped easily, and the service layer handles code generation, TTL checks, and resolution. This separation makes testing simpler and prepares the codebase for future database backends.

* **LRU Cache**
  Two variants are included: one based on a custom linked list/dict structure (to illustrate the O(1) mechanics) and another using Python's `OrderedDict` (for a concise approach). Keeping both demonstrates the trade-offs between explicit implementation and leveraging the standard library.

* **Token Bucket Rate Limiter**
  Implemented with a monotonic clock and floating-point tokens for smooth refill behavior. It ensures bursts are allowed up to capacity while maintaining a steady average rate.

* **Testing Approach**
  Each component has lightweight pytest cases that cover the key behaviors: roundtrip + expiry for the shortener, eviction and ordering for the cache, and refill/limit logic for the token bucket. The tests are small, fast, and directly tied to the intended guarantees of each data structure.

Overall, the goal was to build examples that are **readable, easy to extend, and faithful to the underlying algorithms**, without unnecessary abstraction.

---