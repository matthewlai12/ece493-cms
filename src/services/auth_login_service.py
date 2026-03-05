from typing import Any, TypedDict

from src.services.audit_log import record_event
from src.services.auth_service import authenticate_user, normalize_email
from src.services.user_registration_service import get_user_auth_record


class LoginResult(TypedDict):
    authenticated: bool
    user_email: str
    redirect_to: str | None
    message: str


def login_user(email: str, password: str) -> LoginResult:
    normalized_email = normalize_email(email)
    record = get_user_auth_record(normalized_email)
    if record is None:
        record_event("auth_login", actor=normalized_email or "unknown", details={"success": False})
        raise ValueError("Username or password is incorrect.")

    ok = authenticate_user(
        normalized_email,
        password,
        stored_email=record["email"],
        password_hash=record["password_hash"],
    )
    if not ok:
        record_event("auth_login", actor=normalized_email, details={"success": False})
        raise ValueError("Username or password is incorrect.")

    result: LoginResult = {
        "authenticated": True,
        "user_email": normalized_email,
        "redirect_to": "/dashboard",
        "message": "Login successful.",
    }
    record_event("auth_login", actor=normalized_email, details={"success": True})
    return result


def execute(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload or {}
    result = login_user(str(data.get("email", "")), str(data.get("password", "")))
    return {"service": "auth_login_service", **result}
