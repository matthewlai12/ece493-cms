# Quickstart

## Prerequisites
- Python 3.11
- PostgreSQL

## Setup
1. Create a virtual environment and install dependencies.
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -e ".[dev]"`
2. Configure environment variables:
   - `DATABASE_URL`
   - `STORAGE_BUCKET`
   - `PAYMENT_PROVIDER_KEY`
3. Run database migrations (placeholder):
   - `alembic upgrade head`

## Run
- Start the API server:
  - `uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000`
- Start the web server:
  - `uvicorn src.web.app:app --reload --host 0.0.0.0 --port 8001`
- Access local endpoints:
  - API docs: `http://localhost:8000/docs`
  - API health: `http://localhost:8000/api/health`
  - Web root: `http://localhost:8001/`

## Test
- Baseline compile validation:
  - `python3 -m compileall src tests`
- Run unit and integration tests:
  - `pytest -q`
- If external services are unavailable, validate minimum startup:
  - `python3 -c "from src.api.app import app; print(app.title)"`
