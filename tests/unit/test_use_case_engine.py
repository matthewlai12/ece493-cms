from src.services.use_case_engine import perform_use_case


def test_use_case_engine_core_flows() -> None:
    assert perform_use_case("auth_login_service", {"email": "a@b.com", "password": "x"})["authenticated"]
    assert perform_use_case("auth_password_service", {"new_password": "12345678"})["updated"]

    created = perform_use_case("submission_create_service", {"author_id": "u1", "title": "T"})
    submission_id = str(created["submission"]["id"])
    saved = perform_use_case("submission_save_service", {"submission_id": submission_id, "title": "T2"})
    assert saved["submission"]["status"] == "draft"

    uploaded = perform_use_case("manuscript_upload_service", {"submission_id": submission_id, "filename": "p.pdf"})
    assert uploaded["uploaded"] is True

    invitation = perform_use_case(
        "referee_assign_service",
        {"submission_id": submission_id, "referee_id": "ref-1"},
    )["invitation"]
    invite_id = str(invitation["id"])
    perform_use_case("review_invite_notify_service", {})
    perform_use_case("review_invite_response_service", {"invitation_id": invite_id, "response": "accepted"})
    assignments = perform_use_case("assigned_papers_service", {"referee_id": "ref-1"})
    assert len(assignments["assignments"]) >= 1

    workload = perform_use_case("referee_workload_service", {"referee_id": "ref-1"})
    assert workload["within_limit"] is True

    check_three = perform_use_case("three_referees_service", {"submission_id": submission_id})
    assert "exactly_three" in check_three

    review = perform_use_case("review_submit_service", {"submission_id": submission_id, "score": 4, "comments": "ok"})
    assert review["review"]["status"] == "submitted"
    decision = perform_use_case("decision_record_service", {"submission_id": submission_id, "outcome": "accept"})
    assert decision["decision"]["outcome"] == "accept"
    notified = perform_use_case("decision_notify_service", {"submission_id": submission_id})
    assert notified["notified"] is True


def test_use_case_engine_schedule_and_registration_flows() -> None:
    schedule = perform_use_case("schedule_generate_service", {"sessions": [{"title": "S1"}]})["schedule"]
    schedule_id = str(schedule["id"])
    edited = perform_use_case("schedule_edit_service", {"schedule_id": schedule_id, "sessions": [{"title": "S2"}]})
    assert edited["schedule"]["id"] == int(schedule_id)
    modified = perform_use_case("schedule_modify_service", {"schedule_id": schedule_id, "sessions": [{"title": "S3"}]})
    assert modified["schedule"]["id"] == int(schedule_id)
    published = perform_use_case("schedule_publish_service", {"schedule_id": schedule_id})
    assert published["schedule"]["published"] is True
    assert perform_use_case("schedule_notify_service", {})["notified"] is True
    attendee_view = perform_use_case("schedule_view_attendee_service", {})
    assert isinstance(attendee_view["schedules"], list)

    registration = perform_use_case("conference_register_service", {"attendee_id": "att-1"})["registration"]
    registration_id = str(registration["id"])
    payment = perform_use_case("registration_payment_service", {"registration_id": registration_id, "amount": 10})
    assert payment["payment"]["status"] == "paid"
    confirmation = perform_use_case("payment_confirmation_service", {"registration_id": registration_id})
    assert confirmation["reference_code"].startswith(f"TKT-{registration_id}-")


def test_use_case_engine_default_branch() -> None:
    unknown = perform_use_case("unknown_service", {"x": 1})
    assert unknown["ok"] is True
    assert unknown["payload"] == {"x": 1}
