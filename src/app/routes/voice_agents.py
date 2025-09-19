from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.config.config import settings
from src.classes.classes import manager
import logging

level = logging.INFO if settings.environment == "development" else logging.WARNING

logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Voice Agents"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/ws/voice-agents")
async def voice_agents(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected: {websocket.client}")
    except Exception as e:
        manager.disconnect(websocket)
        logger.error(f"Websocket error: {e}", exc_info=True)
        await websocket.close(code=1011, reason="Internal server error")
