from openai import OpenAI
from typing import Optional
import logging
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "whisper-1"
        self.language = "en"
        self.temperature = 0

    def transcribe(self, file_name: str, prompt: str = "") -> Optional[str]:
        """Transcribe audio file to text"""
        try:
            logger.debug(f"Attempting to transcribe file: {file_name}")
            if not file_name:
                logger.error("No file name provided")
                return None

            with open(file_name, "rb") as audio_file:
                logger.debug("Creating transcription request...")
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    prompt=prompt,
                    language=self.language
                )
                if not response or not response.text:
                    logger.error("Empty response from OpenAI")
                    return None

                transcribed_text = response.text.strip()
                logger.info(f"Transcription successful: {transcribed_text[:50]}...")
                return transcribed_text

        except FileNotFoundError as e:
            logger.error(f"Audio file not found: {file_name}")
            return None
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return None

    def translate(self, file_name: str, prompt: str = "") -> Optional[str]:
        """Translate audio file to English"""
        try:
            with open(file_name, "rb") as audio_file:
                response = self.client.audio.translations.create(
                    model="whisper-1", file=audio_file, prompt=prompt
                )
                return response.text.strip()
        except Exception:
            return None
