from src.services.auth_password_service import change_user_password
from src.services.conference_register_service import register_for_conference, reset_conference_registration_state
from src.services.registration_payment_service import (
    get_latest_payment_for_registration,
    get_payment,
    pay_registration_fee,
    reset_registration_payment_state,
)
from src.services.schedule_modify_service import (
    get_modified_schedule,
    modify_schedule,
    reset_schedule_modify_state,
)
from src.services.schedule_generate_service import generate_schedule, reset_schedule_generate_state
from src.services.schedule_notify_service import (
    assign_presentation_slot,
    get_presentation_slot,
    notify_schedule,
    reset_schedule_notify_state,
)
from src.services.scheduling_engine import generate_schedule as generate_schedule_engine
from src.services.user_registration_service import create_user_account, reset_user_registration_state


def setup_function() -> None:
    reset_user_registration_state()
    reset_conference_registration_state()
    reset_registration_payment_state()
    reset_schedule_generate_state()
    reset_schedule_modify_state()
    reset_schedule_notify_state()


def test_auth_password_validation_branches() -> None:
    create_user_account("a@example.com", "StrongPass1", "A")
    for new_password, expected in [
        ("short", "New password must be at least 8 characters."),
        ("alllowercase1", "New password must include mixed case characters."),
        ("ALLUPPERCASE1", "New password must include mixed case characters."),
        ("NoDigitsHere", "New password must include at least one digit."),
    ]:
        try:
            change_user_password("a@example.com", "StrongPass1", new_password)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError("Expected ValueError")


def test_auth_password_unknown_user_branch() -> None:
    try:
        change_user_password("missing@example.com", "x", "ValidPass1")
    except ValueError as exc:
        assert str(exc) == "Current password is incorrect."
    else:
        raise AssertionError("Expected ValueError")


def test_registration_payment_edge_branches() -> None:
    assert get_payment("x") is None
    assert get_latest_payment_for_registration("x") is None
    assert get_latest_payment_for_registration("1") is None

    register_for_conference("att-1", is_authenticated=True)
    for rid, amount, expected in [
        ("x", 10, "Registration ID is invalid."),
        ("1", 0, "Amount must be greater than zero."),
    ]:
        try:
            pay_registration_fee(registration_id=rid, amount=amount)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError("Expected ValueError")

    # Move to confirmed to hit "not eligible" branch.
    pay_registration_fee(registration_id="1", amount=10.0)
    try:
        pay_registration_fee(registration_id="1", amount=10.0)
    except ValueError as exc:
        assert str(exc) == "Registration is not eligible for payment."
    else:
        raise AssertionError("Expected ValueError")


def test_schedule_modify_validation_branches() -> None:
    generate_schedule(
        schedule_id="50",
        accepted_submissions=[{"submission_id": "5001", "title": "P5001"}],
        rooms=["R1"],
        slot_start="2026-05-01T09:00:00+00:00",
        slot_minutes=30,
    )

    bad_payloads = [
        ([{"submission_id": "x", "title": "T", "room": "R", "start_time": "2026-05-01T09:00:00+00:00", "end_time": "2026-05-01T09:30:00+00:00"}], "Session 1 has an invalid submission_id."),
        ([{"submission_id": "1", "title": "", "room": "R", "start_time": "2026-05-01T09:00:00+00:00", "end_time": "2026-05-01T09:30:00+00:00"}], "Session 1 title is required."),
        ([{"submission_id": "1", "title": "T", "room": "", "start_time": "2026-05-01T09:00:00+00:00", "end_time": "2026-05-01T09:30:00+00:00"}], "Session 1 room is required."),
        ([{"submission_id": "1", "title": "T", "room": "R", "start_time": "", "end_time": ""}], "Session 1 start_time and end_time are required."),
        ([{"submission_id": "1", "title": "T", "room": "R", "start_time": "bad", "end_time": "bad"}], "Session times must be valid ISO-8601 datetimes."),
        ([{"submission_id": "1", "title": "T", "room": "R", "start_time": "2026-05-01T09:30:00+00:00", "end_time": "2026-05-01T09:00:00+00:00"}], "Session 1 start_time must be earlier than end_time."),
    ]
    for sessions, expected in bad_payloads:
        try:
            modify_schedule("50", sessions)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError("Expected ValueError")

    # duplicate submission_id branch
    try:
        modify_schedule(
            "50",
            [
                {"submission_id": "1", "title": "A", "room": "R1", "start_time": "2026-05-01T09:00:00+00:00", "end_time": "2026-05-01T09:30:00+00:00"},
                {"submission_id": "1", "title": "B", "room": "R2", "start_time": "2026-05-01T10:00:00+00:00", "end_time": "2026-05-01T10:30:00+00:00"},
            ],
        )
    except ValueError as exc:
        assert str(exc) == "Each submission can only appear once in a modified schedule."
    else:
        raise AssertionError("Expected ValueError")

    assert get_modified_schedule("x") is None
    assert get_modified_schedule("999") is None


def test_schedule_notify_validation_branches() -> None:
    for args, expected in [
        ({"submission_id": "x", "title": "T", "room": "R", "start_time": "", "end_time": ""}, "Submission ID is invalid."),
        ({"submission_id": "1", "title": "", "room": "R", "start_time": "", "end_time": ""}, "Presentation title is required."),
        ({"submission_id": "1", "title": "T", "room": "", "start_time": "", "end_time": ""}, "Presentation room is required."),
    ]:
        try:
            assign_presentation_slot(**args)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError("Expected ValueError")

    assert get_presentation_slot("x") is None
    assert get_presentation_slot("123") is None
    try:
        notify_schedule("123", "a@example.com")
    except ValueError as exc:
        assert str(exc) == "No presentation schedule is available for this submission."
    else:
        raise AssertionError("Expected ValueError")


def test_scheduling_engine_smoke() -> None:
    assert generate_schedule_engine()["status"] == "generated"
