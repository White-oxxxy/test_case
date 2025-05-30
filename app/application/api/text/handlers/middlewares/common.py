from fastapi import FastAPI

from .metrics import MetricsMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(MetricsMiddleware)