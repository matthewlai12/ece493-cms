from fastapi import APIRouter

from src.api import announcements
from src.api import assigned_papers
from src.api import auth_login
from src.api import auth_password
from src.api import conference_register
from src.api import decision_notify
from src.api import decision_record
from src.api import manuscript_upload
from src.api import payment_confirmation
from src.api import referee_assign
from src.api import referee_workload
from src.api import registration_payment
from src.api import registration_prices
from src.api import registration_validation
from src.api import review_access
from src.api import review_invite_notify
from src.api import review_invite_response
from src.api import review_submit
from src.api import schedule_edit
from src.api import schedule_generate
from src.api import schedule_modify
from src.api import schedule_notify
from src.api import schedule_publish
from src.api import schedule_view
from src.api import schedule_view_attendee
from src.api import submission_create
from src.api import submission_save
from src.api import three_referees
from src.api import user_registration

router = APIRouter(prefix="/api")

@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

router.include_router(announcements.router)
router.include_router(assigned_papers.router)
router.include_router(auth_login.router)
router.include_router(auth_password.router)
router.include_router(conference_register.router)
router.include_router(decision_notify.router)
router.include_router(decision_record.router)
router.include_router(manuscript_upload.router)
router.include_router(payment_confirmation.router)
router.include_router(referee_assign.router)
router.include_router(referee_workload.router)
router.include_router(registration_payment.router)
router.include_router(registration_prices.router)
router.include_router(registration_validation.router)
router.include_router(review_access.router)
router.include_router(review_invite_notify.router)
router.include_router(review_invite_response.router)
router.include_router(review_submit.router)
router.include_router(schedule_edit.router)
router.include_router(schedule_generate.router)
router.include_router(schedule_modify.router)
router.include_router(schedule_notify.router)
router.include_router(schedule_publish.router)
router.include_router(schedule_view.router)
router.include_router(schedule_view_attendee.router)
router.include_router(submission_create.router)
router.include_router(submission_save.router)
router.include_router(three_referees.router)
router.include_router(user_registration.router)
