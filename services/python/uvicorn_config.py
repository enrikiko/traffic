"""Uvicorn settings for the benchmark service.

Tune these through environment variables in Compose or a local shell. Keep
WORKERS=1 when comparing framework overhead; multiple workers measure a
process pool as well as the framework.
"""

import os

import uvicorn


def env_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("UVICORN_HOST", "0.0.0.0"),
        port=int(os.getenv("UVICORN_PORT", "8000")),
        workers=int(os.getenv("UVICORN_WORKERS", "1")),
        loop=os.getenv("UVICORN_LOOP", "auto"),
        http=os.getenv("UVICORN_HTTP", "auto"),
        log_level=os.getenv("UVICORN_LOG_LEVEL", "warning"),
        access_log=env_bool("UVICORN_ACCESS_LOG", False),
        reload=env_bool("UVICORN_RELOAD", False),
        server_header=env_bool("UVICORN_SERVER_HEADER", False),
        date_header=env_bool("UVICORN_DATE_HEADER", False),
    )
