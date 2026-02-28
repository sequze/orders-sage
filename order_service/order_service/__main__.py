import os
import shutil
from pathlib import Path

import uvicorn
from order_service.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "order_service.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )

if __name__ == "__main__":
    main()
