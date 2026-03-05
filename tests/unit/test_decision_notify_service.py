from src.services.audit_log import list_events, reset_events
from src.services.decision_notify_service import (
    notify_author_of_decision,
    reset_decision_notify_state,
    upsert_decision,
)


def setup_function() -> None:
    reset_decision_notify_state()
    reset_events()


def test_notify_author_of_decision_success() -> None:
    upsert_decision(submission_id="1", outcome="accept", decided_by="chair-1")

    result = notify_author_of_decision(submission_id="1", author_email="author@example.com")
    assert result["notified"] is True
    assert result["decision"]["outcome"] == "accept"
    assert list_events("decision_notify")[-1]["details"]["submission_id"] == 1


def test_notify_author_of_decision_requires_decision() -> None:
    try:
        notify_author_of_decision(submission_id="99", author_email="author@example.com")
    except ValueError as exc:
        assert str(exc) == "No decision available for this submission."
    else:
        raise AssertionError("Expected ValueError")
