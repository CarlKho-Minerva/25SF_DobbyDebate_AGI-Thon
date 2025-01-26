from openai import OpenAI
from typing import Optional
from config import TranscriptionConfig


class TranscriptionService:
    def __init__(self, config: TranscriptionConfig):
        self.config = config
        self.client = OpenAI(api_key=config.api_key)

    def transcribe(self, file_name: str, prompt: str = "") -> Optional[str]:
        """Transcribe audio file to text"""
        try:
            with open(file_name, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, prompt=prompt
                )
                return response.text.strip()
        except Exception:
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
