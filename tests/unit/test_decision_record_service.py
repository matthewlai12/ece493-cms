from src.services.audit_log import list_events, reset_events
from src.services.decision_notify_service import reset_decision_notify_state
from src.services.decision_record_service import execute


def setup_function() -> None:
    reset_decision_notify_state()
    reset_events()


def test_decision_record_execute_records_and_notifies() -> None:
    body = execute(
        {
            "submission_id": "2101",
            "outcome": "accept",
            "decided_by": "chair-21",
            "notes": "Strong contribution",
            "author_email": "author21@example.com",
        }
    )
    assert body["decision"]["outcome"] == "accept"
    assert body["notified"] is True
    assert list_events("decision_record")[-1]["details"]["submission_id"] == 2101


def test_decision_record_execute_without_email_does_not_notify() -> None:
    body = execute(
        {
            "submission_id": "2102",
            "outcome": "reject",
            "decided_by": "chair-21",
            "notes": "Needs major revision",
        }
    )
    assert body["notified"] is False
