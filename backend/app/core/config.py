from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "AgentForge AI"
    environment: str = "development"
    database_url: str = "sqlite:///./agentforge.db"
    secret_key: str = "change-this-secret-in-production"
    access_token_expire_minutes: int = 1440
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
settings = Settings()
