from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    access_token_minutes: int = 30
    cookie_secure: bool = False  # set True when served over HTTPS
    # Browsers calling the API from these origins may make write requests (CSRF guard)
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:8000"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()