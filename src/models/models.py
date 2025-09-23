from optparse import Option
from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None


class Agent(BaseModel):
    audio_base64: str
    context: str
    language: str
    user_id: str
    user_conversation_id: str
    questions: List[str]


class TranscriptionGroq(BaseModel):
    audio_base64: str
    language: str


class MessagesGroq(BaseModel):
    role: str
    content: str


class ValidateDataGroq(BaseModel):
    language: str
    current_question: str
    next_question: str
    transcription: str
    expected_type: str


class APIResponseValidationGroq(BaseModel):
    is_response_valid: bool
    normalized_value: Optional[T] = None
    reply_message: str
