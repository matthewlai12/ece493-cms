from src.services.audit_log import list_events, reset_events
from src.services.submission_create_service import create_submission, reset_submission_create_state


def setup_function() -> None:
    reset_submission_create_state()
    reset_events()


def test_create_submission_success() -> None:
    result = create_submission("author-1", "Paper", "Abstract", "pdf")

    assert result["id"] == 1
    assert result["status"] == "submitted"
    assert list_events("submission_create")[-1]["details"]["submission_id"] == 1


def test_create_submission_rejects_unsupported_format() -> None:
    try:
        create_submission("author-1", "Paper", "Abstract", "exe")
    except ValueError as exc:
        assert str(exc) == "Uploaded file format is not supported."
    else:
        raise AssertionError("Expected ValueError")
