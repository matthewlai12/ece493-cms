def test_model_modules_import() -> None:
    import src.models.announcement as announcement
    import src.models.base as base
    import src.models.conferenceregistration as conferenceregistration
    import src.models.confirmationticket as confirmationticket
    import src.models.decision as decision
    import src.models.manuscriptfile as manuscriptfile
    import src.models.payment as payment
    import src.models.registrationprice as registrationprice
    import src.models.review as review
    import src.models.reviewinvitation as reviewinvitation
    import src.models.schedule as schedule
    import src.models.submission as submission
    import src.models.useraccount as useraccount

    assert announcement.Announcement.__tablename__ == "announcement"
    assert base.Base.metadata is not None
    assert conferenceregistration.ConferenceRegistration.__tablename__ == "conferenceregistration"
    assert confirmationticket.ConfirmationTicket.__tablename__ == "confirmationticket"
    assert decision.Decision.__tablename__ == "decision"
    assert manuscriptfile.ManuscriptFile.__tablename__ == "manuscriptfile"
    assert payment.Payment.__tablename__ == "payment"
    assert registrationprice.RegistrationPrice.__tablename__ == "registrationprice"
    assert review.Review.__tablename__ == "review"
    assert reviewinvitation.ReviewInvitation.__tablename__ == "reviewinvitation"
    assert schedule.Schedule.__tablename__ == "schedule"
    assert submission.Submission.__tablename__ == "submission"
    assert useraccount.UserAccount.__tablename__ == "useraccount"
