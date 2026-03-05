from datetime import datetime, timezone
from re import fullmatch
from typing import TypedDict

from src.services.auth_service import hash_password, normalize_email


class RegisteredUser(TypedDict):
    id: int
    email: str
    name: str
    status: str
    created_at: str
    redirect_to: str


_users: list[dict] = []
_email_index: set[str] = set()


def _is_valid_email(email: str) -> bool:
    return bool(fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def create_user_account(email: str, password: str, name: str) -> RegisteredUser:
    normalized_email = normalize_email(email)
    if not _is_valid_email(normalized_email):
        raise ValueError("Invalid email format.")
    if normalized_email in _email_index:
        raise ValueError("Email already registered.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if not name.strip():
        raise ValueError("Name is required.")

    now = datetime.now(timezone.utc).isoformat()
    account = {
        "id": len(_users) + 1,
        "email": normalized_email,
        "password_hash": hash_password(password),
        "name": name.strip(),
        "status": "active",
        "created_at": now,
        "redirect_to": "/login",
    }
    _users.append(account)
    _email_index.add(normalized_email)
    return {
        "id": account["id"],
        "email": account["email"],
        "name": account["name"],
        "status": account["status"],
        "created_at": account["created_at"],
        "redirect_to": account["redirect_to"],
    }


def reset_user_registration_state() -> None:
    _users.clear()
    _email_index.clear()


def get_user_auth_record(email: str) -> dict | None:
    normalized_email = normalize_email(email)
    for user in _users:
        if user["email"] == normalized_email:
            return {"email": user["email"], "password_hash": user["password_hash"], "name": user["name"]}
    return None


def set_user_password_hash(email: str, password_hash: str) -> bool:
    normalized_email = normalize_email(email)
    for user in _users:
        if user["email"] == normalized_email:
            user["password_hash"] = password_hash
            return True
    return False
