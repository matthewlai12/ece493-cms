def send_email(recipient: str, subject: str, body: str) -> dict:
    return {"recipient": recipient, "sent": bool(recipient and subject and body)}
