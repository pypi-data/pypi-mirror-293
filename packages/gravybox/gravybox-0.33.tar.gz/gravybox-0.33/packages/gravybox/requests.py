import httpx
from httpx import AsyncClient

from gravybox.betterstack import collect_logger

logger = collect_logger()

TIMEOUT = 120


class RequestClientWrapper:
    """
    Singleton wrapper for an async http request client
    expects to be initialized once during the FastAPI @app.on_event("startup") hook
    expects to be closed once during the FastAPI @app.on_event("shutdown") hook
    """

    def __init__(self):
        logger.info("initializing request client")
        limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
        timeout = httpx.Timeout(TIMEOUT)
        self.request_client: AsyncClient = AsyncClient(timeout=timeout, limits=limits)

    async def shutdown(self):
        logger.info("shutting down request client")
        await self.request_client.aclose()

    def get_client(self) -> AsyncClient:
        return self.request_client

    @staticmethod
    def initialize():
        global REQUEST_CLIENT_WRAPPER
        REQUEST_CLIENT_WRAPPER = RequestClientWrapper()


REQUEST_CLIENT_WRAPPER: RequestClientWrapper | None = None
