from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.url_shortener.repositories import InMemoryShortUrlRepository
from src.url_shortener.services import ShortenerService, CreateShortUrlRequest

app = FastAPI(title="Mini URL Shortener")

repo = InMemoryShortUrlRepository()
svc = ShortenerService(repo)

class ShortenIn(BaseModel):
    target: str
    ttl_seconds: int | None = None
    custom_code: str | None = None

@app.post("/shorten")
def shorten(payload: ShortenIn):
    s = svc.create(CreateShortUrlRequest(
        target=payload.target,
        ttl_seconds=payload.ttl_seconds,
        custom_code=payload.custom_code
    ))
    return {"code": s.code, "target": s.target, "ttl_seconds": payload.ttl_seconds}

@app.get("/r/{code}")
def resolve(code: str):
    target = svc.resolve(code)
    if not target:
        raise HTTPException(status_code=404, detail="Not found or expired")
    return {"target": target}
