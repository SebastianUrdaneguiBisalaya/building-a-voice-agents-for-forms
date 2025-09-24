from src.config.config import settings
from src.models.models import GreetingGroq, TranscriptionGroq, ValidateDataGroq, MessagesGroq, APIResponseValidationGroq
from groq import Groq, AsyncGroq
import json

_GROQ_CLIENT = Groq(
    api_key=settings.api_groq,
)

_ASYNC_GROQ_CLIENT = AsyncGroq(
    api_key=settings.api_groq,
)


async def greeting_groq(data: GreetingGroq):
    response = await _ASYNC_GROQ_CLIENT.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            MessagesGroq(
                role="system",
                content=(
                    f"You are a helpful assistant taking form responses.\n"
                    f"You just greeted the user and must ask them the first question.\n"
                    f"Your name is Clara.\n"
                    f"The current question is: {data.current_question}.\n"
                    f"The language that you must use is: {data.language}.\n"
                    f"If the questions are not in the same language of {data.language}, you must translate them.\n"
                    f"Example:\n"
                    f"If the current question is 'What is your name?' and the language is Spanish, you must return the question in Spanish.\n"
                    f"'What is your name?' Hola, yo soy Clara, encargada de conducir el siguiente formulario. Empecemos, la primera pregunta es: ¿Cuál es tu nombre?'\n"
                    f"Your greeting should be polite and friendly.\n"
                    f"Important: Output must be plain text only, without Markdown, bold (**), italics, quotes, or any extra symbols.\n"
                ),
            ),
        ],
        temperature=0.3,
        stream=False,
    )
    return response.choices[0].message.content


def transcription_groq(data: TranscriptionGroq):
    transcription = _GROQ_CLIENT.audio.transcriptions.create(
        url=data.audio_base64,
        model="whisper-large-v3-turbo",
        prompt=(
            f"Context:\n"
            f"You are a helpful assistant. Your name is Clara. You must determine language of the audio.\n"
            f"Then, you must translate the audio to {data.language} and return the transcription.\n"
            f"Example:\n"
            f"If the audio is in English, you must return the transcription in {data.language}.\n"
        ),
        response_format="verbose_json",
        language=data.language,
        temperature=0.3,
    )
    return transcription.text.strip()


async def validate_data_groq(data: ValidateDataGroq):
    response = await _ASYNC_GROQ_CLIENT.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            MessagesGroq(
                role="system",
                content=(
                    f"You are a helpful assistant taking form responses.\n"
                    f"The current question is: {data.current_question}.\n"
                    f"The expected type is: {data.expected_type}.\n"
                    f"The next question is: {data.next_question}.\n"
                    f"If the questions are not in the same language of {data.language}, you must translate them.\n"
                    f"The language that you must use is: {data.language}.\n"
                    f"Instructions:\n"
                    f"1. Always validate if the user response matches the expected type.\n"
                    f"2. If valid:\n"
                    f"   - Normalize the value (e.g., 'twenty-four' -> 24, 'juan at gmail dot com' -> 'juan@gmail.com').\n"
                    f"   - Confirm politely to the user.\n"
                    f"   - If there is a next question, include it naturally in the reply.\n"
                    f"   - If there is no next question, thank the user and say the form is complete.\n"
                    f"3. If invalid:\n"
                    f"   - Politely explain why the answer is invalid.\n"
                    f"   - Repeat the current question again, naturally.\n"
                    f"4. Always return JSON only with the following structure:\n"
                    f"{{\n"
                    f"  'is_response_valid': bool,\n"
                    f"  'normalized_value': Any or null,\n"
                    f"  'reply_message': str  # human-like, polite response with either the next or current question\n"
                    f"}}\n"
                    f"Important: Output of 'reply_message' must be plain text only, without Markdown, bold (**), italics, quotes, or any extra symbols.\n"
                )
            ),
            MessagesGroq(
                role="user",
                content=data.transcription,
            ),
        ],
        temperature=0.3,
        stream=False,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "api_response_validation_groq",
                "schema": APIResponseValidationGroq.model_json_schema()
            }
        }
    )
    api_response_validation = APIResponseValidationGroq.model_validate(
        json.loads(response.choices[0].message.content))
    return api_response_validation
