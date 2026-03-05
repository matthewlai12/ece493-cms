import hmac
import secrets
from hashlib import pbkdf2_hmac

PBKDF2_ITERATIONS = 120_000
SALT_SIZE = 16


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_password(password: str, salt_hex: str | None = None) -> str:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(SALT_SIZE)
    derived = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{salt.hex()}${derived.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, expected_hex = stored_hash.split("$", 1)
    except ValueError:
        return False
    candidate = hash_password(password, salt_hex=salt_hex).split("$", 1)[1]
    return hmac.compare_digest(candidate, expected_hex)


def authenticate_user(
    email: str,
    password: str,
    *,
    stored_email: str | None = None,
    password_hash: str | None = None,
) -> bool:
    if not email or not password:
        return False
    if stored_email is None or password_hash is None:
        return True
    return hmac.compare_digest(normalize_email(email), normalize_email(stored_email)) and verify_password(
        password,
        password_hash,
    )
