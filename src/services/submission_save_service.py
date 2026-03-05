from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event

_drafts: dict[int, dict[str, Any]] = {}


class SubmissionDraftResult(TypedDict):
    id: int
    author_id: str
    title: str
    abstract: str
    status: str
    created_at: str
    updated_at: str


def save_submission_progress(
    submission_id: str,
    author_id: str,
    title: str,
    abstract: str,
) -> SubmissionDraftResult:
    if not str(submission_id).isdigit() or int(submission_id) <= 0:
        raise ValueError("Submission ID is invalid.")
    if not author_id.strip():
        raise ValueError("Author ID is required.")

    draft_title = title.strip()
    draft_abstract = abstract.strip()
    if not draft_title and not draft_abstract:
        raise ValueError("At least a title or abstract is required to save progress.")

    sid = int(submission_id)
    now = datetime.now(timezone.utc).isoformat()
    existing = _drafts.get(sid)
    if existing is None:
        created_at = now
    else:
        created_at = str(existing["created_at"])
        if not draft_title:
            draft_title = str(existing["title"])
        if not draft_abstract:
            draft_abstract = str(existing["abstract"])

    item: SubmissionDraftResult = {
        "id": sid,
        "author_id": author_id.strip(),
        "title": draft_title,
        "abstract": draft_abstract,
        "status": "draft",
        "created_at": created_at,
        "updated_at": now,
    }
    _drafts[sid] = item
    record_event("submission_save", actor=item["author_id"], details={"submission_id": sid})
    return item


def get_submission_draft(submission_id: str) -> SubmissionDraftResult | None:
    if not str(submission_id).isdigit():
        return None
    saved = _drafts.get(int(submission_id))
    if saved is None:
        return None
    return dict(saved)


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    saved = save_submission_progress(
        submission_id=str(data.get("submission_id", "")),
        author_id=str(data.get("author_id", "")),
        title=str(data.get("title", "")),
        abstract=str(data.get("abstract", "")),
    )
    return {"service": "submission_save_service", "submission": saved}


def reset_submission_save_state() -> None:
    _drafts.clear()
