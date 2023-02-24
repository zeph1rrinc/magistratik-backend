import pathlib

from fastapi import FastAPI

from . import api

package_name = pathlib.Path(__file__).parent.resolve().name

tags_metadata = []

app = FastAPI(
    title=package_name,
    description="description",
    version="0.1.0",
)

app.include_router(api.router)
