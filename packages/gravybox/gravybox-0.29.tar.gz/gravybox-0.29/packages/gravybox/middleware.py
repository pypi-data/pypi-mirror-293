import time
import traceback

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from gravybox.betterstack import collect_logger
from gravybox.exceptions import GravyboxException

logger = collect_logger()


class LinkEndpoint(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        log_extras = {}
        try:
            link_request = await request.json()
            log_extras["trace_id"] = link_request["trace_id"]
        except Exception as error:
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            logger.error("(!) link failed to parse request", extra=log_extras)
            raise HTTPException(status_code=400, detail="ensure request contains valid json with trace_id")

        logger.info("( ) link request", extra=log_extras)
        start_time = time.time()
        try:
            response = await call_next(request)
            log_extras["elapsed_time"] = time.time() - start_time
            logger.info("(*) link response", extra=log_extras)
            return response
        except Exception as error:
            if isinstance(error, GravyboxException):
                log_extras |= error.log_extras
            log_extras["error_str"] = str(error)
            log_extras["traceback"] = traceback.format_exc()
            log_extras["elapsed_time"] = time.time() - start_time
            logger.error("(!) link failed with unhandled exception", extra=log_extras)
            raise HTTPException(status_code=500, detail="server encountered unhandled exception")
