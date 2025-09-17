from fastapi import APIRouter
from src.config.config import settings
import logging

level = logging.INFO if settings.environment == "development" else logging.WARNING

logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Voice Agents"],
    responses={404: {"description": "Not found"}},
)


@router.get("/voice-agents")
def voice_agents():
    return {"message": "Voice Agents"}
