import asyncio

import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

import src.api.announcements as api_announcements
import src.api.registration_prices as api_registration_prices
import src.api.review_invite_notify as api_review_invite_notify
import src.api.routes as api_routes
import src.api.schedule_view as api_schedule_view
import src.web.review_access as web_review_access
from src.api.assigned_papers import handle_assigned_papers
from src.api.middleware.rbac import require_role
from src.services import audit_log
from src.services.auth_login_service import login_user
from src.services.auth_password_service import change_user_password
from src.services.auth_service import authenticate_user
from src.services.conference_register_service import (
    execute as conference_register_execute,
    get_registration,
    register_for_conference,
    reset_conference_registration_state,
    update_registration_status,
)
from src.services.decision_notify_service import (
    execute as decision_notify_execute,
    notify_author_of_decision,
    reset_decision_notify_state,
)
from src.services.manuscript_upload_service import (
    execute as manuscript_upload_execute,
    list_manuscript_files,
    reset_manuscript_upload_state,
    upload_manuscript,
)
from src.services.payment_confirmation_service import (
    execute as payment_confirmation_execute,
    get_confirmation_ticket,
    issue_confirmation_ticket,
    reset_payment_confirmation_state,
)
from src.services.registration_payment_service import (
    get_latest_payment_for_registration,
    get_payment,
    pay_registration_fee,
    reset_registration_payment_state,
)
from src.services.review_invite_notify_service import (
    count_active_assignments,
    create_review_invitation,
    get_review_invitation,
    reset_review_invite_notify_state,
    update_review_invitation_status,
)
from src.services.review_invite_response_service import respond_to_review_invitation
from src.services.review_submit_service import (
    execute as review_submit_execute,
    list_submitted_reviews,
    reset_review_submit_state,
    submit_review,
)
from src.services.schedule_edit_service import (
    get_schedule,
    reset_schedule_edit_state,
    _to_datetime,
    edit_schedule,
)
from src.services.schedule_generate_service import (
    execute as schedule_generate_execute,
    generate_schedule,
    get_generated_schedule,
    reset_schedule_generate_state,
)
from src.services.schedule_modify_service import get_modified_schedule, modify_schedule, reset_schedule_modify_state
from src.services.schedule_publish_service import (
    get_published_schedule,
    publish_schedule,
    reset_schedule_publish_state,
)
from src.services.submission_create_service import create_submission, execute as submission_create_execute
from src.services.submission_save_service import (
    execute as submission_save_execute,
    get_submission_draft,
    save_submission_progress,
)
from src.services.use_case_engine import perform_use_case
from src.services.user_registration_service import (
    create_user_account,
    get_user_auth_record,
    reset_user_registration_state,
    set_user_password_hash,
)


def setup_function() -> None:
    reset_user_registration_state()
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_payment_confirmation_state()
    reset_decision_notify_state()
    reset_manuscript_upload_state()
    reset_review_invite_notify_state()
    reset_review_submit_state()
    reset_schedule_edit_state()
    reset_schedule_generate_state()
    reset_schedule_modify_state()
    reset_schedule_publish_state()
    audit_log.reset_events()


def _request(path: str, headers: list[tuple[bytes, bytes]] | None = None) -> Request:
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": headers or [],
        "client": ("test", 123),
        "server": ("testserver", 80),
        "scheme": "http",
    }
    return Request(scope)


def test_api_empty_list_branches_and_health(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(api_announcements, "list_public_announcements", lambda: [])
    monkeypatch.setattr(api_registration_prices, "list_active_registration_prices", lambda: [])
    monkeypatch.setattr(api_schedule_view, "get_published_schedule", lambda: None)
    assert api_announcements.handle_announcements()["items"] == []
    assert api_registration_prices.handle_registration_prices()["items"] == []
    assert api_schedule_view.handle_schedule_view()["schedule"] is None
    assert api_routes.health() == {"status": "ok"}


def test_api_assigned_papers_error_and_review_invite_notify_error(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(HTTPException):
        handle_assigned_papers(referee_id="")

    def _raise(_: dict) -> dict:
        raise ValueError("boom")

    monkeypatch.setattr(api_review_invite_notify, "execute", _raise)
    with pytest.raises(HTTPException):
        api_review_invite_notify.handle_review_invite_notify(referee_id="ref-1")


def test_rbac_allows_non_admin_path() -> None:
    async def call_next(_: Request) -> Response:
        return Response("ok", status_code=200)

    response = asyncio.run(require_role(_request("/api/health"), call_next))
    assert response.status_code == 200


def test_web_review_access_requires_editor_id_branch() -> None:
    body = web_review_access.page_review_access(editor_id=None, submission_id="1")
    assert body["query_required"] == "editor_id"


def test_audit_log_list_all_events_branch() -> None:
    audit_log.record_event("x", actor="u")
    all_events = audit_log.list_events()
    assert len(all_events) == 1


def test_auth_login_unknown_user_and_authenticate_user_fallbacks() -> None:
    with pytest.raises(ValueError):
        login_user("missing@example.com", "x")
    assert authenticate_user("a@example.com", "pw", stored_email=None, password_hash=None) is True
    assert authenticate_user("a@example.com", "pw", stored_email="a@example.com", password_hash="bad") is False


def test_auth_password_update_failed_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    create_user_account("u@example.com", "StrongPass1", "U")
    monkeypatch.setattr("src.services.auth_password_service.set_user_password_hash", lambda *_args, **_kwargs: False)
    with pytest.raises(ValueError):
        change_user_password("u@example.com", "StrongPass1", "NewStrong2")


def test_conference_register_extra_branches() -> None:
    with pytest.raises(ValueError):
        register_for_conference(" ", is_authenticated=True)
    with pytest.raises(ValueError):
        register_for_conference("att", is_authenticated=True, pricing_available=False)
    assert get_registration("abc") is None
    assert update_registration_status("abc", "confirmed") is False
    assert update_registration_status("1", " ") is False
    assert conference_register_execute({"attendee_id": "att-1", "is_authenticated": True})["service"] == "conference_register_service"


def test_decision_notify_branches_and_execute() -> None:
    with pytest.raises(ValueError):
        notify_author_of_decision("1", "a@b.com")
    with pytest.raises(ValueError):
        decision_notify_execute({"submission_id": "x", "author_email": "a@b.com"})


def test_manuscript_upload_extra_branches() -> None:
    with pytest.raises(ValueError):
        upload_manuscript("x", "paper.pdf", "application/pdf", b"a")
    with pytest.raises(ValueError):
        upload_manuscript("1", " ", "application/pdf", b"a")
    with pytest.raises(ValueError):
        upload_manuscript("1", "paper.pdf", "application/pdf", b"")
    assert list_manuscript_files("x") == []
    assert manuscript_upload_execute(
        {"submission_id": "2", "filename": "p2.pdf", "content_type": "application/pdf", "content": "abc"}
    )["service"] == "manuscript_upload_service"


def test_payment_confirmation_more_paths() -> None:
    with pytest.raises(ValueError):
        issue_confirmation_ticket("x")
    assert get_confirmation_ticket("x") is None
    assert get_confirmation_ticket("1") is None
    with pytest.raises(ValueError):
        payment_confirmation_execute({"registration_id": "x"})


def test_registration_payment_lookup_paths() -> None:
    register_for_conference("att-10", is_authenticated=True)
    pay_registration_fee("1", amount=50.0)
    assert get_payment("1") is not None
    assert get_latest_payment_for_registration("1") is not None


def test_review_invite_notify_and_response_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError):
        create_review_invitation("x", "ref", "Title", "Abs", "r@example.com")
    with pytest.raises(ValueError):
        create_review_invitation("1", "", "Title", "Abs", "r@example.com")
    with pytest.raises(ValueError):
        create_review_invitation("1", "ref", "", "Abs", "r@example.com")

    created = create_review_invitation("1", "ref-1", "T1", "A1", "r1@example.com")
    invitation_id = str(created["invitation"]["id"])
    assert count_active_assignments(" ref-1 ") >= 1
    assert get_review_invitation("x") is None
    assert update_review_invitation_status("x", "accepted") is None

    with pytest.raises(ValueError):
        respond_to_review_invitation(invitation_id, "maybe")

    monkeypatch.setattr("src.services.review_invite_response_service.update_review_invitation_status", lambda *_args, **_kwargs: None)
    with pytest.raises(ValueError):
        respond_to_review_invitation(invitation_id, "accept")


def test_review_submit_and_submission_services_extra_branches() -> None:
    with pytest.raises(ValueError):
        submit_review("x", "ref", 3, "ok")
    with pytest.raises(ValueError):
        submit_review("1", "", 3, "ok")
    with pytest.raises(ValueError):
        submit_review("1", "ref", 3, " ")
    submit_review("1", "ref", 4, "ok")
    assert len(list_submitted_reviews("1")) == 1
    assert review_submit_execute({"submission_id": "2", "referee_id": "r2", "score": 5, "comments": "great"})["service"] == "review_submit_service"

    with pytest.raises(ValueError):
        create_submission("", "Title", "Abstract", "pdf")
    with pytest.raises(ValueError):
        create_submission("a", "", "Abstract", "pdf")
    with pytest.raises(ValueError):
        create_submission("a", "Title", "", "pdf")
    assert submission_create_execute(
        {"author_id": "a", "title": "T", "abstract": "A", "manuscript_format": "pdf"}
    )["service"] == "submission_create_service"

    with pytest.raises(ValueError):
        save_submission_progress("x", "a", "T", "A")
    with pytest.raises(ValueError):
        save_submission_progress("1", "", "T", "A")
    assert get_submission_draft("x") is None
    assert get_submission_draft("1") is None
    assert submission_save_execute({"submission_id": "1", "author_id": "a", "title": "T"})["service"] == "submission_save_service"


def test_schedule_services_extra_branches() -> None:
    with pytest.raises(ValueError):
        _to_datetime("bad", "start_time")
    with pytest.raises(ValueError):
        edit_schedule("1", [])
    with pytest.raises(ValueError):
        edit_schedule(
            "1",
            [{"title": "", "room": "R", "start_time": "2026-01-01T09:00:00+00:00", "end_time": "2026-01-01T09:30:00+00:00"}],
        )
    with pytest.raises(ValueError):
        edit_schedule(
            "1",
            [{"title": "T", "room": "", "start_time": "2026-01-01T09:00:00+00:00", "end_time": "2026-01-01T09:30:00+00:00"}],
        )
    with pytest.raises(ValueError):
        edit_schedule("1", [{"title": "T", "room": "R", "start_time": "", "end_time": ""}])
    assert get_schedule("x") is None
    assert get_schedule("999") is None

    with pytest.raises(ValueError):
        generate_schedule("1", [{"submission_id": "1", "title": "T"}], ["R"], "bad", 30)
    with pytest.raises(ValueError):
        generate_schedule("1", [{"submission_id": "1", "title": "T"}], [], "2026-01-01T09:00:00+00:00", 30)
    with pytest.raises(ValueError):
        generate_schedule("1", [{"submission_id": "1", "title": "T"}], ["R"], "2026-01-01T09:00:00+00:00", 0)
    with pytest.raises(ValueError):
        generate_schedule("1", [{"submission_id": "1", "title": ""}], ["R"], "2026-01-01T09:00:00+00:00", 30)
    assert get_generated_schedule("x") is None
    assert get_generated_schedule("999") is None
    assert schedule_generate_execute(
        {
            "schedule_id": "20",
            "accepted_submissions": [{"submission_id": "101", "title": "T101"}],
            "rooms": ["R1"],
            "slot_start": "2026-01-01T09:00:00+00:00",
            "slot_minutes": 30,
        }
    )["service"] == "schedule_generate_service"

    with pytest.raises(ValueError):
        modify_schedule("20", [])
    assert get_modified_schedule("2") is None

    with pytest.raises(ValueError):
        publish_schedule("999", finalized=True, recipients=[])
    generate_schedule("30", [{"submission_id": "301", "title": "T301"}], ["R1"], "2026-01-01T09:00:00+00:00", 30)
    assert publish_schedule("30", finalized=True, recipients=[])["schedule"]["status"] == "published"


def test_schedule_publish_empty_sessions_and_get_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    generate_schedule("31", [{"submission_id": "311", "title": "T311"}], ["R1"], "2026-01-01T09:00:00+00:00", 30)
    monkeypatch.setattr(
        "src.services.schedule_publish_service.get_generated_schedule",
        lambda _sid: {"id": 31, "status": "draft", "generated_at": "x", "sessions": []},
    )
    with pytest.raises(ValueError):
        publish_schedule("31", finalized=True, recipients=[])

    assert get_published_schedule("x") is None
    assert get_published_schedule("999") is None


def test_user_registration_auth_record_and_set_password_branches() -> None:
    assert get_user_auth_record("missing@example.com") is None
    assert set_user_password_hash("missing@example.com", "hash") is False


def test_use_case_engine_remaining_branches() -> None:
    save_new = perform_use_case("submission_save_service", {"submission_id": "not-a-number", "title": "Draft"})
    assert save_new["submission"]["status"] == "draft"

    edited = perform_use_case("schedule_edit_service", {"schedule_id": "abc", "sessions": [{"title": "S"}]})
    assert edited["schedule"]["status"] == "draft"
    published = perform_use_case("schedule_publish_service", {"schedule_id": "def"})
    assert published["schedule"]["published"] is True

    perform_use_case("review_submit_service", {"submission_id": "1", "score": 3, "comments": "ok"})
    perform_use_case("review_submit_service", {"submission_id": "2", "score": 4, "comments": "ok2"})
    filtered = perform_use_case("review_access_service", {"submission_id": "2"})
    assert len(filtered["reviews"]) == 1
