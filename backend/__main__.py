import uvicorn

from .app import package_name
from .settings import settings


def main():
    uvicorn.run(
        f"{package_name}.app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
