from src.api.decision_notify import handle_decision_notify
from src.api.decision_record import handle_decision_record
from src.services.decision_notify_service import reset_decision_notify_state


def test_decision_notify_reflects_recorded_decision() -> None:
    reset_decision_notify_state()
    handle_decision_record(
        submission_id="4",
        payload={"outcome": "reject", "decided_by": "chair-2", "notes": "Insufficient novelty"},
    )

    body = handle_decision_notify(
        submission_id="4",
        payload={"author_email": "author4@example.com"},
    )
    assert body["decision"]["outcome"] == "reject"
    assert body["decision"]["notes"] == "Insufficient novelty"
    assert body["recipient"] == "author4@example.com"
