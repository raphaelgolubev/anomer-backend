import uvicorn

from src.settings import settings, test


def main():
    test()

    uvicorn.run(
        app="src.app:app",
        host=settings.server.host, # type: ignore
        port=settings.server.port, # type: ignore
        lifespan="on",
        reload=True,
    )


if __name__ == "__main__":
    main()