import base64
import models
from fastapi import HTTPException
from src.lib.groq import transcription_groq, processing_data_groq


def agent(data: models.Agent):
    """
    """
    if not validate_base64(data.audio_base64):
        raise HTTPException(
            status_code=400,
            detail="Invalid audio base64 string",
        )
    try:
        transcription = transcription_groq(models.TranscriptionGroq(
            audio_base64=data.audio_base64,
            language=data.language,
        ))
        if not transcription:
            raise HTTPException(
                status_code=204,
                detail="No transcription found",
            )
        response = processing_data_groq(models.ProcessingDataGroq(
            language=data.language,
            questions=data.questions,
            transcription=transcription,
        ))
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {e}",
        )


def validate_base64(base64_str: str) -> bool:
    """Validates whether the given base64 string is valid.
    Args:
            str: The base64 string to validate.
    Returns:
            bool: True if the base64 string is valid, False otherwise.
    """
    try:
        base64.b64decode(base64_str, validate=True)
        return True
    except Exception:
        return False
