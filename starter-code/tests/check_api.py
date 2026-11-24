"""Bootstrap smoke checks and one example of a scenario acceptance test."""

import argparse
import json
import os
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = os.getenv("DEMO_URL", "http://127.0.0.1:8080").rstrip("/")


def request(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if data is not None else {}
    try:
        response = urlopen(
            Request(BASE_URL + path, data, headers, method=method), timeout=5
        )
    except HTTPError as error:
        response = error
    with response:
        content = response.read()
        return response.status, json.loads(content) if content else None


class SmokeChecks(unittest.TestCase):
    def test_api_ready_through_frontend(self):
        self.assertEqual(request("/health"), (200, {"status": "ok"}))

    def test_seeded_items_and_claimants(self):
        status, items = request("/api/found-items")
        self.assertEqual(status, 200)
        self.assertEqual(
            {item["id"] for item in items}, {"ITEM-01", "ITEM-02", "ITEM-03"}
        )
        for item in items:
            self.assertEqual(
                set(item), {"id", "description", "storage_point", "status"}
            )
        status, claimants = request("/api/claimants")
        self.assertEqual(status, 200)
        self.assertEqual(
            {person["id"] for person in claimants}, {"CLAIMANT-01", "CLAIMANT-02"}
        )

    def test_item_lookup(self):
        status, item = request("/api/found-items/ITEM-01")
        self.assertEqual(status, 200)
        self.assertEqual(item["description"], "Folded umbrella")
        self.assertNotIn("proof_colour", item)
        status, error = request("/api/found-items/ITEM-99")
        self.assertEqual(status, 404)
        self.assertEqual(error["error"]["code"], "NOT_FOUND")


class ClaimChecks(unittest.TestCase):
    def test_us01_wrong_proof_preserves_state(self):
        item_path = "/api/found-items/ITEM-03"
        item_before = request(item_path)
        self.assertEqual(item_before[0], 200)
        self.assertEqual(
            item_before[1]["status"], "AVAILABLE", "Start with clean seed data."
        )
        claims_before = request("/api/claims")

        status, error = request(
            "/api/claims",
            "POST",
            {
                "item_id": "ITEM-03",
                "claimant_id": "CLAIMANT-01",
                "proof_colour": "purple",
            },
        )
        self.assertEqual(status, 409, f"Expected PROOF_MISMATCH, got {error}")
        self.assertEqual(error["error"]["code"], "PROOF_MISMATCH")
        self.assertEqual(request(item_path), item_before)
        self.assertEqual(claims_before[0], 200)
        self.assertEqual(request("/api/claims"), claims_before)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="check only the supplied read-only bootstrap",
    )
    smoke_only = parser.parse_args().smoke

    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromTestCase(SmokeChecks)
    if not smoke_only:
        suite.addTests(loader.loadTestsFromTestCase(ClaimChecks))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
