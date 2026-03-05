from src.config.settings import Settings
from src.services.service_utils import build_service_response


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.database_url
    assert settings.storage_bucket
    assert settings.payment_provider_key


def test_build_service_response_delegates_engine() -> None:
    body = build_service_response("auth_login_service", {"email": "test@example.com", "password": "pw"})
    assert body["service"] == "auth_login_service"
    assert "authenticated" in body
