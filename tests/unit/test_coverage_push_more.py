import asyncio

import pytest
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

import src.api.announcements as api_announcements
import src.api.registration_prices as api_registration_prices
import src.api.review_invite_notify as api_review_invite_notify
import src.api.schedule_view as api_schedule_view
from src.api.middleware.rbac import require_role
from src.services.auth_service import authenticate_user
from src.services.review_invite_notify_service import (
    create_review_invitation,
    reset_review_invite_notify_state,
    update_review_invitation_status,
)
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_modify_service import get_modified_schedule, modify_schedule, reset_schedule_modify_state
from src.services.use_case_engine import perform_use_case
from src.web.review_access import page_review_access


def setup_function() -> None:
    reset_review_invite_notify_state()
    reset_schedule_generate_state()
    reset_schedule_modify_state()


def _build_request(path: str) -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
            "client": ("test", 0),
            "server": ("testserver", 80),
            "scheme": "http",
        }
    )


def test_api_empty_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(api_announcements, "list_public_announcements", lambda: [])
    monkeypatch.setattr(api_registration_prices, "list_active_registration_prices", lambda: [])
    monkeypatch.setattr(api_schedule_view, "get_published_schedule", lambda: None)

    assert api_announcements.handle_announcements()["message"] == "No public announcements available."
    assert api_registration_prices.handle_registration_prices()["message"] == "Registration price list is not available."
    assert api_schedule_view.handle_schedule_view()["message"] == "Conference schedule has not been published."


def test_review_invite_notify_http_exception_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise(_: dict) -> dict:
        raise ValueError("forced")

    monkeypatch.setattr(api_review_invite_notify, "execute", _raise)
    with pytest.raises(HTTPException):
        api_review_invite_notify.handle_review_invite_notify(referee_id="ref-x")


def test_rbac_non_admin_path_calls_next() -> None:
    async def call_next(_: Request) -> Response:
        return Response("ok", status_code=200)

    resp = asyncio.run(require_role(_build_request("/api/health"), call_next))
    assert resp.status_code == 200


def test_web_review_access_query_required_branch() -> None:
    body = page_review_access(editor_id=None, submission_id="1")
    assert body["query_required"] == "editor_id"


def test_schedule_modify_get_existing_schedule_branch() -> None:
    generate_schedule(
        schedule_id="70",
        accepted_submissions=[{"submission_id": "7001", "title": "P7001"}],
        rooms=["R1"],
        slot_start="2026-06-01T09:00:00+00:00",
        slot_minutes=30,
    )
    modify_schedule(
        "70",
        [
            {
                "submission_id": "7001",
                "title": "P7001",
                "room": "R1",
                "start_time": "2026-06-01T09:00:00+00:00",
                "end_time": "2026-06-01T09:30:00+00:00",
            }
        ],
    )
    assert get_modified_schedule("70") is not None


def test_review_invitation_update_not_found_and_auth_malformed_hash_branch() -> None:
    create_review_invitation("1", "ref-1", "T1", "A1", "r1@example.com")
    assert update_review_invitation_status("999", "accepted") is None
    assert authenticate_user("a@example.com", "pw", stored_email="a@example.com", password_hash="invalid") is False


def test_use_case_engine_branches_for_schedule_publish_create_and_review_filter() -> None:
    created_publish = perform_use_case("schedule_publish_service", {"schedule_id": "abc"})
    assert created_publish["schedule"]["published"] is True

    perform_use_case("review_submit_service", {"submission_id": "10", "score": 4, "comments": "ok"})
    perform_use_case("review_submit_service", {"submission_id": "11", "score": 4, "comments": "ok"})
    filtered = perform_use_case("review_access_service", {"submission_id": "11"})
    assert len(filtered["reviews"]) == 1
