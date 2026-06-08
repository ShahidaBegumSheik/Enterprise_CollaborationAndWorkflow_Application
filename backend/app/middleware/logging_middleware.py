import time

from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        start = time.time()

        logger.info(f"Request started: {request.method} {request.url.path}")

        response = await call_next(request)

        duration = round(time.time() - start, 3)

        logger.info(
            f"Request completed: "
            f"{request.method} {request.url.path} "
            f"Status={response.status_code} "
            f"Duration={duration}s"
        )

        return response