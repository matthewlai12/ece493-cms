from src.api.decision_notify import handle_decision_notify
from src.api.decision_record import handle_decision_record
from src.services.decision_notify_service import reset_decision_notify_state


def test_decision_notify_endpoint() -> None:
    reset_decision_notify_state()
    handle_decision_record(
        submission_id="1",
        payload={"outcome": "accept", "decided_by": "chair-1"},
    )

    body = handle_decision_notify(
        submission_id="1",
        payload={"author_email": "author@example.com"},
    )
    assert body["service"] == "decision_notify_service"
    assert body["notified"] is True
    assert body["decision"]["submission_id"] == 1
