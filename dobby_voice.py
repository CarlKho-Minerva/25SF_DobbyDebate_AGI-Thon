from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, voices
import os
from typing import Optional
from config import ELEVENLABS_API_KEY


def init_eleven_labs() -> Optional[ElevenLabs]:
    """Initialize ElevenLabs client"""
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        return client
    except Exception as e:
        print(f"Error initializing ElevenLabs: {e}")
        return None


def list_available_voices(client: ElevenLabs):
    """List all available voices"""
    try:
        available_voices = voices()
        print("\nAvailable voices:")
        for voice in available_voices:
            print(f"- {voice.name} (ID: {voice.voice_id})")
    except Exception as e:
        print(f"Error listing voices: {e}")


def text_to_speech(
    text: str,
    voice_id: str = "lE5ZJB6jGeeuvSNxOvs2",  # Marshal (annoying) voice
    model_id: str = "eleven_turbo_v2_5",
) -> Optional[bytes]:
    """Convert text to speech using ElevenLabs"""
    client = init_eleven_labs()
    if not client:
        return None

    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128",
        )
        return audio
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None


def demo_voice():
    """Demonstration of ElevenLabs text-to-speech"""
    print("\n=== ElevenLabs Text-to-Speech Demo ===")

    client = init_eleven_labs()
    if not client:
        return

    # Show available voices
    list_available_voices(client)

    # Test messages
    messages = [
        "Hello! I am Dobby, your AI assistant. How can I help you today?",
        "That's an interesting question. Let me think about it.",
        "I apologize, but I cannot assist with that request.",
    ]

    # Try each message
    for msg in messages:
        print(f"\nConverting: {msg}")
        audio = text_to_speech(msg)
        if audio:
            print("Playing audio...")
            play(audio)
            input("Press Enter to continue to next message...")


if __name__ == "__main__":
    demo_voice()
