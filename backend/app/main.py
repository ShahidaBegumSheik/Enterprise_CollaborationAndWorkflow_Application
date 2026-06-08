from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.api import api_router
from app.core.rate_limit import limiter
import app.models
from fastapi_pagination import add_pagination

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(LoggingMiddleware)


app.include_router(api_router, prefix=settings.api_v1_prefix)
add_pagination(app)


@app.get("/")
def health_check():
    return {"message": "Mini Enterprise Flow backend running"}

