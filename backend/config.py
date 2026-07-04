from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str = "your-gemini-api-key"
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "ticket_agent"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
