"""Read seeded data from PostgreSQL without exposing proof colours."""

import psycopg
from psycopg.rows import dict_row


class PostgresDeskReads:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def _read(self, query: str, values: tuple = ()) -> list[dict]:
        with psycopg.connect(self.database_url, row_factory=dict_row, connect_timeout=3) as connection:
            return connection.execute(query, values).fetchall()

    def ready(self) -> bool:
        try:
            self._read("SELECT id FROM found_items LIMIT 1")
            return True
        except psycopg.Error:
            return False

    def found_items(self) -> list[dict]:
        return self._read(
            "SELECT id, description, storage_point, status FROM found_items ORDER BY id"
        )

    def found_item(self, item_id: str) -> dict | None:
        rows = self._read(
            "SELECT id, description, storage_point, status FROM found_items WHERE id = %s",
            (item_id,),
        )
        return rows[0] if rows else None

    def claimants(self) -> list[dict]:
        return self._read("SELECT id, name FROM claimants ORDER BY id")
