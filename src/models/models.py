from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None


class TranscriptionGroq(BaseModel):
    audio_base64: str
    language: str


class MessagesGroq(BaseModel):
    role: str
    content: str


class GreetingGroq(BaseModel):
    language: str
    current_question: str


class ValidateDataGroq(BaseModel):
    language: str
    current_question: str
    next_question: Optional[str] = None
    transcription: str
    expected_type: str


class APIResponseValidationGroq(BaseModel):
    is_response_valid: bool
    normalized_value: Optional[T] = None
    reply_message: str
