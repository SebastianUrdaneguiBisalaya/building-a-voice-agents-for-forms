from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from src.config.config import settings
from src.classes.classes import manager, FormSession
from src.lib.groq import greeting_groq, transcription_groq, validate_data_groq
from src.models.models import GreetingGroq, TranscriptionGroq, ValidateDataGroq
import logging

level = logging.INFO if settings.environment == "development" else logging.WARNING

logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Voice Agents"],
    responses={404: {"description": "Not found"}},
)

sessions: Dict[str, FormSession] = {}


@router.websocket("/ws/voice-agents")
async def voice_agents(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        user_id = websocket.query_params.get("user_id")
        language = websocket.query_params.get("language")
        print(user_id, language)
        sessions[user_id] = FormSession([
                                        {"key": "age", "question": "What is your age?",
                                            "type": "int"},
                                        {"key": "email", "question": "What is your email?",
                                            "type": "str"},
                                        {"key": "phone", "question": "What is your phone number?",
                                            "type": "str"},
                                        ])
        session = sessions[user_id]
        greeting = await greeting_groq(GreetingGroq(
            language=language,
            current_question=session.current_question()['question'],
        ))
        await websocket.send_text(greeting)
        while True:
            data = await websocket.receive_json()
            audio_base_64 = data.get("audio")
            if not audio_base_64:
                await websocket.send_text("No audio received")
                continue
            transcription = transcription_groq(
                TranscriptionGroq(
                    audio_base64=audio_base_64,
                    language=language,
                )
            )
            current_question = session.current_question()
            next_question = None if session.current_index + \
                1 >= len(session.questions) else session.questions[session.current_index + 1]
            result = await validate_data_groq(ValidateDataGroq(
                language=language,
                current_question=current_question["question"],
                next_question=next_question["question"] if next_question else None,
                transcription=transcription,
                expected_type=current_question["type"],
            ))
            if not result.is_response_valid:
                await websocket.send_json({
                    "message": f"{result.reply_message}",
                })
                continue
            session.record_answer(
                current_question["key"], result.normalized_value)
            if session.completed:
                await websocket.send_json({
                    "message": f"{result.reply_message}",
                    "answers": session.answers,
                })
                break
            else:
                next_question = session.current_question()
                await websocket.send_json({
                    "message": f"{result.reply_message}",
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected: {websocket.client}")
    except Exception as e:
        manager.disconnect(websocket)
        logger.error(f"Websocket error: {e}", exc_info=True)
        await websocket.close(code=1011, reason="Internal server error")
