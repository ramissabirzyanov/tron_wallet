from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения, загружаемых из переменных окружения.
    """
    DATABASE_URL: str
    TRON_NETWORK: str = "shasta"  # чтобы протестировать в swagger

    model_config = SettingsConfigDict(
        env_file=".env",
    )

settings = Settings()
