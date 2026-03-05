from fastapi import APIRouter

from src.web import announcements
from src.web import assigned_papers
from src.web import auth_login
from src.web import auth_password
from src.web import conference_register
from src.web import decision_notify
from src.web import decision_record
from src.web import manuscript_upload
from src.web import payment_confirmation
from src.web import referee_assign
from src.web import referee_workload
from src.web import registration_payment
from src.web import registration_prices
from src.web import registration_validation
from src.web import review_access
from src.web import review_invite_notify
from src.web import review_invite_response
from src.web import review_submit
from src.web import schedule_edit
from src.web import schedule_generate
from src.web import schedule_modify
from src.web import schedule_notify
from src.web import schedule_publish
from src.web import schedule_view
from src.web import schedule_view_attendee
from src.web import submission_create
from src.web import submission_save
from src.web import three_referees
from src.web import user_registration

router = APIRouter()

@router.get("/")
def index() -> dict:
    return {"status": "web-ok"}

router.include_router(announcements.router, prefix="/web")
router.include_router(assigned_papers.router, prefix="/web")
router.include_router(auth_login.router, prefix="/web")
router.include_router(auth_password.router, prefix="/web")
router.include_router(conference_register.router, prefix="/web")
router.include_router(decision_notify.router, prefix="/web")
router.include_router(decision_record.router, prefix="/web")
router.include_router(manuscript_upload.router, prefix="/web")
router.include_router(payment_confirmation.router, prefix="/web")
router.include_router(referee_assign.router, prefix="/web")
router.include_router(referee_workload.router, prefix="/web")
router.include_router(registration_payment.router, prefix="/web")
router.include_router(registration_prices.router, prefix="/web")
router.include_router(registration_validation.router, prefix="/web")
router.include_router(review_access.router, prefix="/web")
router.include_router(review_invite_notify.router, prefix="/web")
router.include_router(review_invite_response.router, prefix="/web")
router.include_router(review_submit.router, prefix="/web")
router.include_router(schedule_edit.router, prefix="/web")
router.include_router(schedule_generate.router, prefix="/web")
router.include_router(schedule_modify.router, prefix="/web")
router.include_router(schedule_notify.router, prefix="/web")
router.include_router(schedule_publish.router, prefix="/web")
router.include_router(schedule_view.router, prefix="/web")
router.include_router(schedule_view_attendee.router, prefix="/web")
router.include_router(submission_create.router, prefix="/web")
router.include_router(submission_save.router, prefix="/web")
router.include_router(three_referees.router, prefix="/web")
router.include_router(user_registration.router, prefix="/web")
