from re import fullmatch


def validate_registration_payload(payload: dict) -> dict:
    errors: list[str] = []
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not name:
        errors.append("Name is required.")
    if not fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        errors.append("Invalid email format.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if password.lower() == password or password.upper() == password:
        errors.append("Password must include mixed case characters.")
    if not any(ch.isdigit() for ch in password):
        errors.append("Password must include at least one digit.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "normalized": {"name": name, "email": email},
    }
