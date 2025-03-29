from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENROUTER_URL: str
    OPENROUTER_API_KEY: str
    HUGGINGFACE_TOKEN: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
