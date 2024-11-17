from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    BOOST_TAP_NAME: str
    BOOST_MAXIMIZER_NAME: str
    BOOST_CHARGER_NAME: str

    ADMIN_AUTH_TOKEN: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    SECRET_KEY: str

    TELEGRAM_BOT_TOKEN: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env.dev")


settings = Settings()
