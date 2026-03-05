from src.services.audit_log import list_events, reset_events
from src.services.manuscript_upload_service import reset_manuscript_upload_state, upload_manuscript


def setup_function() -> None:
    reset_manuscript_upload_state()
    reset_events()


def test_upload_manuscript_success() -> None:
    result = upload_manuscript(
        submission_id="1",
        filename="paper.pdf",
        content_type="application/pdf",
        content_bytes=b"abc",
    )

    assert result["id"] == 1
    assert result["storage_key"].startswith("submissions/1/")
    assert list_events("manuscript_upload")[-1]["details"]["file_id"] == 1


def test_upload_manuscript_invalid_format() -> None:
    try:
        upload_manuscript(
            submission_id="1",
            filename="paper.exe",
            content_type="application/x-msdownload",
            content_bytes=b"abc",
        )
    except ValueError as exc:
        assert str(exc) == "File format is not supported."
    else:
        raise AssertionError("Expected ValueError")
