from src.web.decision_notify import submit_decision_notify
from src.web.decision_record import submit_decision_record
from src.web.manuscript_upload import submit_manuscript_upload
from src.web.payment_confirmation import submit_payment_confirmation
from src.web.registration_payment import submit_registration_payment
from src.web.review_invite_response import submit_review_invite_response
from src.web.schedule_edit import submit_schedule_edit
from src.web.schedule_modify import submit_schedule_modify
from src.web.schedule_publish import submit_schedule_publish
from src.web.submission_save import submit_submission_save
from src.web.user_registration import submit_user_registration
from src.services.conference_register_service import reset_conference_registration_state
from src.services.decision_notify_service import reset_decision_notify_state
from src.services.payment_confirmation_service import reset_payment_confirmation_state
from src.services.registration_payment_service import reset_registration_payment_state
from src.services.review_invite_notify_service import create_review_invitation, reset_review_invite_notify_state
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_modify_service import reset_schedule_modify_state
from src.services.schedule_publish_service import reset_schedule_publish_state
from src.services.schedule_edit_service import reset_schedule_edit_state
from src.services.submission_save_service import reset_submission_save_state
from src.services.user_registration_service import reset_user_registration_state
from src.api.conference_register import handle_conference_register


def setup_function() -> None:
    reset_decision_notify_state()
    reset_review_invite_notify_state()
    reset_schedule_generate_state()
    reset_schedule_edit_state()
    reset_schedule_modify_state()
    reset_schedule_publish_state()
    reset_submission_save_state()
    reset_user_registration_state()
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_payment_confirmation_state()


def test_web_submit_handlers_success_paths() -> None:
    decision = submit_decision_record("1", {"outcome": "accept", "decided_by": "chair", "author_email": "a@b.com"})
    assert decision["service"] == "decision_record_service"
    notify = submit_decision_notify("1", {"author_email": "a@b.com"})
    assert notify["service"] == "decision_notify_service"

    manuscript = submit_manuscript_upload("1", {"filename": "p.pdf", "content_type": "application/pdf", "content": "abc"})
    assert manuscript["service"] == "manuscript_upload_service"

    invite = create_review_invitation("1", "ref-1", "Paper", "Abs", "ref@example.com")["invitation"]
    response = submit_review_invite_response(str(invite["id"]), {"response": "accept"})
    assert response["service"] == "review_invite_response_service"

    edited = submit_schedule_edit(
        "1",
        {
            "sessions": [{"title": "S1", "room": "R1", "start_time": "2026-05-01T09:00:00+00:00", "end_time": "2026-05-01T09:30:00+00:00", "submission_id": 1}],
        },
    )
    assert edited["service"] == "schedule_edit_service"

    generate_schedule("2", [{"submission_id": "2", "title": "Paper 2"}], ["R2"], "2026-05-01T10:00:00+00:00", 30)
    modified = submit_schedule_modify(
        "2",
        {
            "sessions": [{"submission_id": 2, "title": "Paper 2", "room": "R2", "start_time": "2026-05-01T10:00:00+00:00", "end_time": "2026-05-01T10:30:00+00:00"}],
        },
    )
    assert modified["service"] == "schedule_modify_service"

    generate_schedule("3", [{"submission_id": "3", "title": "Paper 3"}], ["R3"], "2026-05-01T11:00:00+00:00", 30)
    published = submit_schedule_publish("3", {"finalized": True, "recipients": []})
    assert published["service"] == "schedule_publish_service"

    saved = submit_submission_save("10", {"author_id": "a1", "title": "Draft"})
    assert saved["service"] == "submission_save_service"

    user = submit_user_registration({"name": "User", "email": "user@example.com", "password": "StrongPass1"})
    assert user["message"] == "registered"

    reg = handle_conference_register({"attendee_id": "att-1", "attendee_email": "att@example.com", "is_authenticated": True})
    reg_id = str(reg["registration"]["id"])
    payment = submit_registration_payment(reg_id, {"amount": 100.0, "attendee_email": "att@example.com"})
    assert payment["service"] == "registration_payment_service"

    ticket = submit_payment_confirmation(reg_id, {"attendee_email": "att@example.com"})
    assert ticket["service"] == "payment_confirmation_service"
