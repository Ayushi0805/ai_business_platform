from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    N8N_WEBHOOK_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
