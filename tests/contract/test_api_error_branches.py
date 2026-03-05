from fastapi import HTTPException

from src.api.assigned_papers import handle_assigned_papers
from src.api.decision_notify import handle_decision_notify
from src.api.decision_record import handle_decision_record
from src.api.referee_assign import handle_referee_assign
from src.api.referee_workload import handle_referee_workload
from src.api.review_access import handle_review_access
from src.api.review_invite_notify import handle_review_invite_notify
from src.api.review_invite_response import handle_review_invite_response
from src.api.schedule_notify import handle_schedule_notify
from src.api.three_referees import handle_three_referees
from src.services.review_invite_notify_service import reset_review_invite_notify_state
from src.services.review_submit_service import reset_review_submit_state


def _assert_raises_http_400(fn, *args, **kwargs) -> None:
    try:
        fn(*args, **kwargs)
    except HTTPException as exc:
        assert exc.status_code in {400, 401}
    else:
        raise AssertionError("Expected HTTPException")


def test_api_error_handlers_cover_branches() -> None:
    reset_review_invite_notify_state()
    reset_review_submit_state()

    _assert_raises_http_400(handle_assigned_papers, referee_id="")
    _assert_raises_http_400(handle_decision_notify, submission_id="1", payload={"author_email": ""})
    _assert_raises_http_400(handle_decision_record, submission_id="1", payload={"outcome": "maybe"})
    _assert_raises_http_400(
        handle_referee_assign,
        payload={"submission_id": "", "referee_id": "", "paper_title": "", "paper_abstract": "", "referee_email": ""},
    )
    _assert_raises_http_400(handle_referee_workload, payload={"referee_id": "", "requested_new_assignments": -1})
    _assert_raises_http_400(handle_review_access, editor_id="", submission_id=None)
    # Empty referee_id is accepted by this endpoint and returns all invitations.
    body = handle_review_invite_notify(referee_id="")
    assert body["service"] == "review_invite_notify_service"
    _assert_raises_http_400(handle_review_invite_response, invitation_id="999", payload={"response": "accept"})
    _assert_raises_http_400(handle_schedule_notify, payload={"submission_id": "x", "author_email": "x@y.com"})
    _assert_raises_http_400(handle_three_referees, payload={"submission_id": "x"})
