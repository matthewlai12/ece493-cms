from src.api.submission_save import handle_submission_save
from src.services.submission_save_service import get_submission_draft, reset_submission_save_state


def test_submission_save_endpoint() -> None:
    reset_submission_save_state()

    body = handle_submission_save(
        submission_id="1",
        payload={
            "author_id": "author-1",
            "title": "Draft title",
            "abstract": "Draft abstract",
        },
    )
    assert body["service"] == "submission_save_service"
    assert body["submission"]["status"] == "draft"

    saved = get_submission_draft("1")
    assert saved is not None
    assert saved["title"] == "Draft title"
    assert saved["abstract"] == "Draft abstract"
