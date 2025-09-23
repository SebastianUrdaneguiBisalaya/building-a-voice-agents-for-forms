from src.config.config import settings
from groq import Groq, AsyncGroq
import models
import json

_GROQ_CLIENT = Groq(
    api_key=settings.api_groq,
)

_ASYNC_GROQ_CLIENT = AsyncGroq(
    api_key=settings.api_groq,
)


def transcription_groq(data: models.TranscriptionGroq):
    transcription = _GROQ_CLIENT.audio.transcriptions.create(
        url=data.audio_base64,
        model="whisper-large-v3-turbo",
        prompt=(
            f"Context: "
            f"You are a helpful assistant. You must determine language of the audio. "
            f"Then, you must translate the audio to {data.language} and return the transcription. "
            f"Example: "
            f"If the audio is in English, you must return the transcription in {data.language}. "
        ),
        response_format="verbose_json",
        language=data.language,
        temperature=0.3,
    )
    return transcription.text.strip()


async def validate_data_groq(data: models.ValidateDataGroq):
    response = await _ASYNC_GROQ_CLIENT.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            models.MessagesGroq(
                role="system",
                content=(
                    f"You are a helpful assistant taking form responses.\n"
                    f"The current question is: {data.current_question}.\n"
                    f"The expected type is: {data.expected_type}.\n"
                    f"The next question is: {data.next_question}.\n"
                    f"The language that you must use is: {data.language}.\n"
                    f"Instructions:\n"
                    f"1. Check if the user response matches the expected type.\n"
                    f"2. If valid -> normalize the value and generate a natural reply that thanks the user"
                    f" and smoothly transitions to the next question if provided.\n"
                    f"3. If invalid -> return a polite correction message that reminds the user what question was.\n"
                    f"4. Always return JSON only with the following structure:\n"
                    f"{{\n"
                    f"	'is_response_valid': bool,\n"
                    f"	'normalized_value': Any or null,\n"
                    f"	'reply_message': str # natural, human-like response to the user, polite response to user,\n"
                    f"}}\n"
                )
            ),
            models.MessagesGroq(
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
                "schema": models.APIResponseValidationGroq.model_json_schema()
            }
        }
    )
    api_response_validation = models.APIResponseValidationGroq.model_validate(
        json.loads(response.choices[0].message.content))
    return api_response_validation
