from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.auth_service import hash_password, normalize_email, verify_password
from src.services.user_registration_service import get_user_auth_record, set_user_password_hash


class PasswordChangeResult(TypedDict):
    updated: bool
    user_email: str
    message: str


def _validate_new_password(new_password: str) -> None:
    if len(new_password) < 8:
        raise ValueError("New password must be at least 8 characters.")
    if new_password.lower() == new_password or new_password.upper() == new_password:
        raise ValueError("New password must include mixed case characters.")
    if not any(ch.isdigit() for ch in new_password):
        raise ValueError("New password must include at least one digit.")


def change_user_password(email: str, current_password: str, new_password: str) -> PasswordChangeResult:
    normalized_email = normalize_email(email)
    record = get_user_auth_record(normalized_email)
    if record is None:
        record_event("auth_password", actor=normalized_email or "unknown", details={"success": False})
        raise ValueError("Current password is incorrect.")

    if not verify_password(current_password, record["password_hash"]):
        record_event("auth_password", actor=normalized_email, details={"success": False})
        raise ValueError("Current password is incorrect.")

    _validate_new_password(new_password)
    ok = set_user_password_hash(normalized_email, hash_password(new_password))
    if not ok:
        record_event("auth_password", actor=normalized_email, details={"success": False})
        raise ValueError("Password update failed.")

    record_event("auth_password", actor=normalized_email, details={"success": True})
    return {
        "updated": True,
        "user_email": normalized_email,
        "message": "Password updated successfully.",
    }


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = change_user_password(
        str(data.get("email", "")),
        str(data.get("current_password", "")),
        str(data.get("new_password", "")),
    )
    return {"service": "auth_password_service", **result}
