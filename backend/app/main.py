"""Compose the application and register shared HTTP error responses."""

import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.application.service import DeskService, build_service
from app.presentation.api import error_response, routes


def create_app(service: DeskService | None = None) -> FastAPI:
    if service is None:
        service = build_service(os.environ["DATABASE_URL"])

    app = FastAPI(title="Campus Lost Property Desk", docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.include_router(routes(service))

    @app.exception_handler(RequestValidationError)
    async def invalid_input(_request: Request, _exc: RequestValidationError):
        return error_response(400, "INVALID_INPUT", "Supply a valid JSON object with the required fields.")

    @app.exception_handler(NotImplementedError)
    async def unfinished(_request: Request, _exc: NotImplementedError):
        return error_response(501, "SCENARIO_TODO", "Implement the claim workflow in the scenario brief.")

    return app


app = create_app()
