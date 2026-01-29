import uvicorn

from src.settings import settings
from src.utils.test_funcs import test_settings


def main():
    test_settings()

    uvicorn.run(
        app="src.app:app",
        host=settings.server.host, # type: ignore
        port=settings.server.port, # type: ignore
        lifespan="on",
        reload=True,
    )


if __name__ == "__main__":
    main()