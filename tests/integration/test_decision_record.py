from src.api.decision_record import handle_decision_record
from src.services.decision_notify_service import get_decision, reset_decision_notify_state


def test_decision_record_endpoint() -> None:
    reset_decision_notify_state()
    body = handle_decision_record(
        submission_id="1",
        payload={"outcome": "accept", "decided_by": "chair"},
    )
    assert body["service"] == "decision_record_service"
    saved = get_decision("1")
    assert saved is not None
    assert saved["outcome"] == "accept"
