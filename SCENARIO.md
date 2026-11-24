# Demo Scenario 01 — Campus Lost Property Desk

A campus reception desk stores items found in teaching buildings. Students need to find matching descriptions and claim items. Desk staff need to verify a claim and record collection so that one item can be handed to only one claimant. Build a service-oriented application with a browser frontend, backend API and persistent database. The starter uses FastAPI, PostgreSQL, vanilla JavaScript and Nginx. The contract is independent of that stack.

## User stories and acceptance criteria

### US-01 — Find and request a found item

As a claimant, I want to browse descriptions and supply a private identifying detail so I can request an item that is mine.

- **Given** a known claimant, an available item and a matching proof colour, **when** I submit the claim form, **then** the claim becomes `REQUESTED`, the item becomes `HELD` and I can retrieve the claim.
- **Given** an item is held or collected, **when** I request it, **then** I see that it is unavailable and no second claim is created. Two competing valid requests for one available item create at most one claim.
- **Given** a known claimant and an available item, **when** I submit the wrong proof colour, **then** I see a rejection and the item stays available. The response never reveals the expected colour.
- **Given** a missing or malformed field or an unknown reference, **when** I submit the form, **then** I see an error and no claim is created.

### US-02 — Verify a requested claim

As a desk assistant, I want to confirm a requested claim after checking the claimant's description so that the handover desk can recognise an approved claim.

- **Given** a `REQUESTED` claim, **when** I verify it, **then** the claim becomes `VERIFIED`, the item stays `HELD` and the desk view shows the new claim state.
- **Given** a claim in another state, **when** I attempt to verify it, **then** I see a state conflict and neither record changes.

### US-03 — Record collection

As a desk assistant, I want to record the handover of a verified item so that others can see that it has been collected.

- **Given** a `VERIFIED` claim, **when** I record collection, **then** the claim and item both become `COLLECTED` and remain visible in their respective views.
- **Given** a claim in another state, **when** I attempt collection, **then** I see a state conflict and neither record changes.

### US-04 — Cancel a pending request

As a claimant, I want to cancel my pending request so another person can request the item.

- **Given** a `REQUESTED` claim, **when** I cancel it, **then** it becomes `CANCELLED`, remains retrievable and releases its item to `AVAILABLE`.
- **Given** a verified, collected or cancelled claim, **when** I attempt cancellation, **then** I see a state conflict and neither record changes.
- **Given** an unknown claim ID, **when** I look it up or cancel it, **then** I see a not-found error.

## Technical contract

### Responsibilities, data and screens

The inventory responsibility reads found-item descriptions and tracks availability. The intake responsibility validates the claimant and checks proof at request time. The desk responsibility manages verification, handover and cancellation. Explain how these responsibilities interact across the frontend, backend and database. The backend owns the state transitions.

Persist found items, claimants and claims. Each claim references one claimant and one item. An item can have at most one active claim in `REQUESTED` or `VERIFIED`. Save claim and item changes atomically, including under competing requests. Preserve cancelled and collected records. A found item's status is `AVAILABLE`, `HELD` or `COLLECTED`. Only an available item can be claimed. A claim is `REQUESTED`, `VERIFIED`, `COLLECTED` or `CANCELLED`. The expected proof colour belongs to the item record and stays on the server. Omit it from browser data, API responses and logs. Use fictional claimants and colours. The classroom exercise uses a visible role switch or separate views and has no authentication requirement.

Provide a browser list and detail view with current item status, a form for claimant, item and proof colour, and a desk queue with claim detail and controls for verification, collection and eligible cancellation. Views may share one page. Show the saved state or a useful rejection message after each action. A rejected action must leave the previous state visible or reload it from the API.

### Required seed data

| ID | Description or name | Storage point | Expected proof colour | Initial status |
| --- | --- | --- | --- | --- |
| `ITEM-01` | Folded umbrella | North reception | `red` | `AVAILABLE` |
| `ITEM-02` | Insulated bottle | Library desk | `blue` | `AVAILABLE` |
| `ITEM-03` | Zipped pencil case | North reception | `green` | `AVAILABLE` |
| `CLAIMANT-01` | Mira Vale | | | |
| `CLAIMANT-02` | Dev Lin | | | |

Start with no claims. Initialise the schema and test fixtures automatically on an empty database. The starter supplies `database/schema.sql` and `database/seed.sql` for the item and claimant records. Extend the schema to persist claims and their constraints.

### HTTP API

All IDs are nonblank strings. The server generates a unique claim ID. For creation, accept a JSON object with exactly `item_id`, `claimant_id` and `proof_colour`, each a nonblank string with no leading or trailing whitespace. Colour matching is case-sensitive. Check input, look up the references, check item availability, then compare the proof colour. The verify, collect and cancel actions take no request body. For those actions, look up the claim before checking its state. Return errors as `{"error":{"code":"<code>","message":"<explanation>"}}` and keep secrets and stack traces out of responses.

| Method and path | Success | Published errors |
| --- | --- | --- |
| `GET /health` | `200 {"status":"ok"}` when the API and database are ready | `503 NOT_READY` otherwise |
| `GET /api/claimants` | `200`, array of claimants | |
| `GET /api/found-items` | `200`, array of items | |
| `GET /api/found-items/{id}` | `200`, item | `404 NOT_FOUND` |
| `POST /api/claims` | `201`, claim in `REQUESTED`. Item becomes `HELD`. | `400 INVALID_INPUT` for invalid JSON, wrong keys or invalid values. `404 NOT_FOUND` for an unknown item or claimant. `409 ITEM_UNAVAILABLE` for an unavailable item. `409 PROOF_MISMATCH` for incorrect proof. |
| `GET /api/claims` | `200`, array of claims, including closed records. `[]` when empty. | |
| `GET /api/claims/{id}` | `200`, claim | `404 NOT_FOUND` |
| `POST /api/claims/{id}/verify` | `200`, claim in `VERIFIED`. Item remains `HELD`. | `404 NOT_FOUND`, `409 INVALID_TRANSITION` outside `REQUESTED` |
| `POST /api/claims/{id}/collect` | `200`, claim in `COLLECTED`. Item becomes `COLLECTED`. | `404 NOT_FOUND`, `409 INVALID_TRANSITION` outside `VERIFIED` |
| `DELETE /api/claims/{id}` | `204`, empty body. Item becomes `AVAILABLE` and the claim is retrievable as `CANCELLED`. | `404 NOT_FOUND`, `409 INVALID_TRANSITION` outside `REQUESTED` |

A found-item object has `id`, `description`, `storage_point` and `status`. A claimant object has `id` and `name`. A claim object has `id`, `item_id`, `claimant_id` and `status`. All listed fields are strings. The list order and generated IDs may vary.

On fresh data, posting `{"item_id":"ITEM-01","claimant_id":"CLAIMANT-01","proof_colour":"red"}` creates a claim such as `{"id":"CLAIM-EXAMPLE","item_id":"ITEM-01","claimant_id":"CLAIMANT-01","status":"REQUESTED"}`. The colour is never returned.

## Verification

Start the project with `docker compose up --build`. From another terminal, run `bash tests/run.sh` against the running stack. Keep the frontend and API URLs in the project README. Use a fresh database for destructive or terminal cases, or allocate separate fixture records for each case. Restart without clearing the database when checking persistence. See the [student guide](STUDENT-GUIDE.md) for what the starter already verifies and which tests to add.

| Scope | Setup, action and expected result |
| --- | --- |
| Runtime and read contract | Start the three services from empty storage. Expect `200` and status `ok` at `/health`. List both claimants and all three items. Retrieve `ITEM-01` as available and expect `404 NOT_FOUND` for `ITEM-99`. Confirm the proof colour is absent from the item responses. |
| US-01, successful request | Submit the example request. Expect `201`, the generated ID and `REQUESTED`. Retrieve the claim from the detail and collection endpoints. Confirm the item is `HELD`. |
| US-01, validation and availability | On separate clean fixtures, use the wrong colour for `409 PROOF_MISMATCH`, `ITEM-99` or `CLAIMANT-99` for `404 NOT_FOUND`, and malformed JSON, an extra key or a numeric colour for `400 INVALID_INPUT`. Check no claim is added and the item state is unchanged. Request an item that is already held or collected and expect `409 ITEM_UNAVAILABLE`. Send two valid requests concurrently for one available item and expect exactly one `201` and one `409 ITEM_UNAVAILABLE`. |
| US-02, verification | Verify a fresh requested claim. Expect `200 VERIFIED` and a held item. Repeat verification and expect `409 INVALID_TRANSITION` with unchanged records. |
| US-03, handover | Try collecting before verification and expect `409 INVALID_TRANSITION`. Verify, collect and expect `200 COLLECTED` for the claim and a collected item. Repeat collection and expect `409 INVALID_TRANSITION`. Restart the stack with the same volume and confirm both records still show `COLLECTED`. |
| US-04, cancellation | Cancel a requested claim. Expect `204` with no body, a retrievable `CANCELLED` claim and an available item. Confirm a new claim for that item succeeds. Attempt to cancel each of a verified, collected and cancelled claim and expect `409 INVALID_TRANSITION`. Retrieve and cancel `CLAIM-99` and expect `404 NOT_FOUND`. |
| Browser | Submit a wrong colour and observe rejection. Correct it, submit the request, verify it and record collection through the browser. Confirm that the item and claim status update after each action and that the final state remains after reload. |
| CI and evidence | Run the backend and frontend pull request checks on a reviewed change. Open one failing run, identify the failing step and show the successful retest. Merge to `main` and confirm the integration workflow builds both images and runs the smoke and full checks for that revision. The unfinished claim produces an expected failure in the full suite. Record AI assistance and a diagnosis in the supplied evidence files. |

Use the [classroom workflow steps](STUDENT-GUIDE.md) and [AI evidence guide](AI-EVIDENCE.md) for the CI/CD exercise. The [rubric](RUBRIC.md) is a reference for an optional, larger scenario implementation.
