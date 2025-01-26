from typing import Tuple, Optional
from .audio_service import AudioService
from .chat_service import ChatService
import logging

logger = logging.getLogger(__name__)

class DobbyService:
    def __init__(self):
        self.audio_service = AudioService()
        self.chat_service = ChatService()

    def process_debate_turn(self, topic: str) -> Tuple[Optional[str], Optional[str], Optional[bytes]]:
        """
        Handle one turn of debate
        Returns: (transcription, response_text, audio_bytes)
        """
        try:
            # Record and transcribe user's speech
            transcription = self.audio_service.record_and_transcribe(seconds=5)
            if not transcription:
                logger.error("Failed to transcribe user speech")
                return None, None, None

            # Generate Dobby's response
            response = self.chat_service.generate_response(
                topic=topic,
                user_input=transcription
            )
            if not response:
                logger.error("Failed to generate response")
                return transcription, None, None

            # Convert response to speech
            audio = self.audio_service.text_to_speech(response)
            if not audio:
                logger.error("Failed to generate speech")
                return transcription, response, None

            return transcription, response, audio

        except Exception as e:
            logger.error(f"Error in debate turn: {str(e)}")
            return None, None, None

    def validate_topic(self, topic: str) -> bool:
        """Validate if topic is appropriate for debate"""
        return bool(topic) and len(topic.strip()) > 0
