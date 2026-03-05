# Development Notes

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run services

```bash
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
uvicorn src.web.app:app --reload --host 0.0.0.0 --port 8001
```

## Validate baseline

```bash
python3 -m compileall src tests
# Optional once pytest is installed:
pytest -q
```
