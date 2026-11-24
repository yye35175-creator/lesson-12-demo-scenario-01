"""Translate HTTP requests into application calls."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.application.service import DeskService


def error_response(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def routes(service: DeskService) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health():
        if not service.ready():
            return error_response(503, "NOT_READY", "The database is not ready.")
        return {"status": "ok"}

    @router.get("/api/found-items")
    def found_items():
        return service.found_items()

    @router.get("/api/found-items/{item_id}")
    def found_item(item_id: str):
        item = service.found_item(item_id)
        if item is None:
            return error_response(404, "NOT_FOUND", "Found item does not exist.")
        return item

    @router.get("/api/claimants")
    def claimants():
        return service.claimants()

    @router.post("/api/claims", status_code=201)
    def request_claim(body: dict):
        return service.claims_todo()

    @router.get("/api/claims")
    def claims():
        return service.claims_todo()

    @router.get("/api/claims/{claim_id}")
    def claim(claim_id: str):
        return service.claims_todo()

    @router.post("/api/claims/{claim_id}/verify")
    def verify_claim(claim_id: str):
        return service.claims_todo()

    @router.post("/api/claims/{claim_id}/collect")
    def collect_claim(claim_id: str):
        return service.claims_todo()

    @router.delete("/api/claims/{claim_id}", status_code=204)
    def cancel_claim(claim_id: str):
        return service.claims_todo()

    return router
