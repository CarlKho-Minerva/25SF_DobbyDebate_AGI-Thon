from openai import OpenAI
from typing import Optional
from config import OPENAI_API_KEY


class TranscriptionService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "whisper-1"
        self.language = "en"
        self.temperature = 0

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
