from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_ALLOWED_FORMATS = {"pdf", "docx"}
_submissions: list[dict] = []


class SubmissionResult(TypedDict):
    id: int
    author_id: str
    title: str
    abstract: str
    status: str
    manuscript_format: str
    created_at: str


def create_submission(author_id: str, title: str, abstract: str, manuscript_format: str) -> SubmissionResult:
    if not author_id.strip():
        raise ValueError("Author ID is required.")
    if not title.strip():
        raise ValueError("Title is required.")
    if not abstract.strip():
        raise ValueError("Abstract is required.")

    normalized_format = manuscript_format.strip().lower()
    if normalized_format not in _ALLOWED_FORMATS:
        raise ValueError("Uploaded file format is not supported.")

    item: SubmissionResult = {
        "id": len(_submissions) + 1,
        "author_id": author_id.strip(),
        "title": title.strip(),
        "abstract": abstract.strip(),
        "status": "submitted",
        "manuscript_format": normalized_format,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _submissions.append(item)
    record_event("submission_create", actor=item["author_id"], details={"submission_id": item["id"]})
    return item


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    submission = create_submission(
        author_id=str(data.get("author_id", "")),
        title=str(data.get("title", "")),
        abstract=str(data.get("abstract", "")),
        manuscript_format=str(data.get("manuscript_format", "")),
    )
    return {"service": "submission_create_service", "submission": submission}


def reset_submission_create_state() -> None:
    _submissions.clear()
