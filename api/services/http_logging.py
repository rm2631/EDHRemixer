import logging
import time
from typing import Any, Optional


def logged_get(
    client: Any,
    url: str,
    *,
    logger: logging.Logger,
    service: str,
    attempt: Optional[int] = None,
    max_attempts: Optional[int] = None,
    **kwargs: Any,
):
    """Perform client.get(url, **kwargs) and log the outbound call.

    Headers and bodies are intentionally never logged.
    """
    attempt_info = f" (attempt {attempt}/{max_attempts})" if attempt else ""
    params = kwargs.get("params")
    logger.info(
        "-> %s GET %s%s params=%s",
        service,
        url,
        attempt_info,
        params if params else "-",
    )
    start = time.perf_counter()
    try:
        response = client.get(url, **kwargs)
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.error(
            "<- %s GET %s FAILED after %.0fms: %s: %s",
            service,
            url,
            elapsed_ms,
            type(e).__name__,
            e,
        )
        raise
    elapsed_ms = (time.perf_counter() - start) * 1000
    level = logging.INFO if response.status_code < 400 else logging.WARNING
    logger.log(
        level,
        "<- %s GET %s status=%s %.0fms bytes=%s",
        service,
        url,
        response.status_code,
        elapsed_ms,
        len(response.content) if response.content is not None else 0,
    )
    return response
