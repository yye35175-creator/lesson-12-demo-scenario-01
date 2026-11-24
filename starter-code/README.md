# Campus Lost Property Desk — starter code

Use this folder as the root of a practice repository. Copy its contents, including `.github/`, into the repository root. The [scenario](../SCENARIO.md) describes the optional feature extension, and the [student guide](../STUDENT-GUIDE.md) describes the Lesson 12 CI/CD exercise.

## Run the starter

Start a Docker engine, leave ports 8000 and 8080 free, and run from this folder:

```sh
docker compose config
docker compose up --build -d --wait
bash tests/run.sh --smoke
```

Open `http://127.0.0.1:8080` to inspect the inventory and claim form. The API listens at `http://127.0.0.1:8000` and exposes documentation at `/api/docs`. Nginx serves the browser files and proxies `/api/` and `/health` to the backend. The database starts with fictional items and claimants. Use `docker compose logs frontend backend database` to diagnose startup failures and `docker compose down` to stop the stack. The database volume persists between runs; use a fresh Compose project name when you need clean seed data.

On Windows, `python tests/check_api.py --smoke` works without Bash. The smoke tests check the running stack. The full `bash tests/run.sh` also includes a deliberately failing US-01 wrong-proof test: claim routes return `501 SCENARIO_TODO` until you implement the optional claim workflow.

## Project map

| Path | Purpose |
| --- | --- |
| `backend/` | FastAPI application and backend image recipe; Compose builds it from the repository root. |
| `frontend/` | Nginx image recipe, browser files and proxy configuration; Compose builds it from `frontend/`. |
| `database/` | PostgreSQL schema and seed fixtures. |
| `tests/` | Smoke checks and the optional claim acceptance example. |
| `templates/ai-evidence.md` | Record AI assistance and verification. |
| `evidence/debug-log.md` | Record a failed check, diagnosis and retest. |
| `.github/` | Pull request and issue templates; add the Lesson 12 workflows yourself. |

In Lesson 12, write two pull request workflows that check the code before building each image. Then write an integration workflow that builds both images on pushes to `main`, runs the smoke tests and reproduces the full suite's expected claim failure. Follow the [student guide](../STUDENT-GUIDE.md).
