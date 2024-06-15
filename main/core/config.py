from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str

    # keys
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    # Database
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_NAME: str

    # Configuration
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_DISCOVERY_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
