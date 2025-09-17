from src.config.config import settings
from groq import Groq

groq = Groq(
    api_key=settings.api_groq,
)
