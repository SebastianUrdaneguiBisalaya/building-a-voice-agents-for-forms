import os
from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.join(os.path.dirname(__file__), ".."))

load_dotenv(BASE_DIR)


class Settings(BaseSettings):
    environment: str = Field(..., alias="ENVIRONMENT")
    api_groq: str = Field(..., alias="API_GROQ")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def get_settings():
    try:
        settings = Settings()
        return settings
    except ValidationError as e:
        print(f"The environment variables are not set. {e}")
        raise e


settings = get_settings()
