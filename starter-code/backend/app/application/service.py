"""Coordinate the inventory and claim use cases."""

from app.domain.ports import DeskReads
from app.infrastructure.postgres import PostgresDeskReads


class DeskService:
    def __init__(self, reads: DeskReads):
        self.reads = reads

    def ready(self) -> bool:
        return self.reads.ready()

    def found_items(self) -> list[dict]:
        return self.reads.found_items()

    def found_item(self, item_id: str) -> dict | None:
        return self.reads.found_item(item_id)

    def claimants(self) -> list[dict]:
        return self.reads.claimants()

    def claims_todo(self):
        # Add claim persistence, proof validation and domain transition rules.
        raise NotImplementedError


def build_service(database_url: str) -> DeskService:
    return DeskService(PostgresDeskReads(database_url))
