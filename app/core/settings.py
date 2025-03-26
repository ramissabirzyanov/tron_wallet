from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения, загружаемых из переменных окружения.
    """
    DATABASE_URL: str
    TRON_NETWORK: str = "mainnet"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
