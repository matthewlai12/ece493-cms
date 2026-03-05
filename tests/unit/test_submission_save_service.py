from src.services.audit_log import list_events, reset_events
from src.services.submission_save_service import (
    get_submission_draft,
    reset_submission_save_state,
    save_submission_progress,
)


def setup_function() -> None:
    reset_submission_save_state()
    reset_events()


def test_save_submission_progress_success() -> None:
    result = save_submission_progress(
        submission_id="3",
        author_id="author-3",
        title="Draft title",
        abstract="Draft abstract",
    )

    assert result["id"] == 3
    assert result["status"] == "draft"
    assert get_submission_draft("3") is not None
    assert list_events("submission_save")[-1]["details"]["submission_id"] == 3


def test_save_submission_progress_preserves_existing_fields() -> None:
    save_submission_progress(
        submission_id="2",
        author_id="author-2",
        title="Initial title",
        abstract="Initial abstract",
    )

    updated = save_submission_progress(
        submission_id="2",
        author_id="author-2",
        title="",
        abstract="Updated abstract",
    )
    assert updated["title"] == "Initial title"
    assert updated["abstract"] == "Updated abstract"


def test_save_submission_progress_requires_some_content() -> None:
    try:
        save_submission_progress(
            submission_id="1",
            author_id="author-1",
            title="   ",
            abstract="",
        )
    except ValueError as exc:
        assert str(exc) == "At least a title or abstract is required to save progress."
    else:
        raise AssertionError("Expected ValueError")
