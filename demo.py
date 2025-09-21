from src.url_shortener.repositories import InMemoryShortUrlRepository
from src.url_shortener.services import ShortenerService, CreateShortUrlRequest

if __name__ == "__main__":
    repo = InMemoryShortUrlRepository()
    svc = ShortenerService(repo)
    created = svc.create(CreateShortUrlRequest(target="https://github.com"))
    print("Short code:", created.code)
    print("Resolve ->", svc.resolve(created.code))
