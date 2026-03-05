from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./cms.db"
    storage_bucket: str = "cms-manuscripts"
    payment_provider_key: str = "dev-key"


settings = Settings()
