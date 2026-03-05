from datetime import datetime, timezone
from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.storage_client import store_file

_ALLOWED_CONTENT_TYPES = {"application/pdf"}
_MAX_SIZE_BYTES = 10 * 1024 * 1024
_files: list[dict] = []


class ManuscriptUploadResult(TypedDict):
    id: int
    submission_id: int
    filename: str
    content_type: str
    size_bytes: int
    storage_key: str
    uploaded_at: str


def upload_manuscript(
    submission_id: str,
    filename: str,
    content_type: str,
    content_bytes: bytes,
) -> ManuscriptUploadResult:
    if not str(submission_id).isdigit():
        raise ValueError("Submission ID is invalid.")
    if not filename.strip():
        raise ValueError("Filename is required.")
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise ValueError("File format is not supported.")
    if len(content_bytes) == 0:
        raise ValueError("File is empty.")
    if len(content_bytes) > _MAX_SIZE_BYTES:
        raise ValueError("File exceeds maximum size limit.")

    storage_key = f"submissions/{submission_id}/{filename.strip()}"
    stored = store_file(storage_key, content_bytes)
    item: ManuscriptUploadResult = {
        "id": len(_files) + 1,
        "submission_id": int(submission_id),
        "filename": filename.strip(),
        "content_type": content_type,
        "size_bytes": int(stored["size_bytes"]),
        "storage_key": str(stored["storage_key"]),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    _files.append(item)
    record_event("manuscript_upload", actor=f"submission:{submission_id}", details={"file_id": item["id"]})
    return item


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    content = str(data.get("content", "")).encode("utf-8")
    file_info = upload_manuscript(
        submission_id=str(data.get("submission_id", "")),
        filename=str(data.get("filename", "")),
        content_type=str(data.get("content_type", "application/pdf")),
        content_bytes=content,
    )
    return {"service": "manuscript_upload_service", "file": file_info}


def list_manuscript_files(submission_id: str = "") -> list[ManuscriptUploadResult]:
    if submission_id and str(submission_id).isdigit():
        sid = int(submission_id)
        return [dict(item) for item in _files if int(item["submission_id"]) == sid]
    return [dict(item) for item in _files]


def reset_manuscript_upload_state() -> None:
    _files.clear()
