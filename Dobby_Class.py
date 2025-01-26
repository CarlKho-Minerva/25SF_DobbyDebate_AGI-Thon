# Built-in imports
import subprocess
import json
import os
import wave
import tempfile
import time

# External package imports - with error handling
try:
    import pyaudio
except ImportError:
    print("Error: pyaudio not installed. Run: pip install pyaudio")
    print("On MacOS, you may need to first run: brew install portaudio")
    raise

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip not installed. Run: pip install pyperclip")
    raise

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai not installed. Run: pip install openai")
    raise

from config import (
    API_KEY,
    OPENAI_API_KEY,
    URL,
    MODEL,
    TEMP_DIR,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_CHUNK_SIZE,
    AUDIO_FORMAT,
    AUDIO_DEFAULT_DURATION,
)


def extract_content(response: dict) -> str:
    """Extract just the content from the API response"""
    if not response or "choices" not in response:
        return None
    return response["choices"][0]["message"]["content"]


def send_chat_message(message_content: str) -> str:
    """Send a chat message to the API and return just the response content"""
    system_prompt = """You are Dobby, an aggressive and passionate AI debater. Clever burn comebacks.
    Your responses should follow the SEXI template:
    1. State your position clearly.
    2. Explain your reasoning with strong, assertive arguments
    3. Provide concrete eXamples or evidence to support your position
    4. Describe the Impact or importance of your argument

    You respond briefly. Presidentail debate basically. Keep the aggressive swearing Dobby in though. Be conversational level brief and to the point. Burn but dont overdo it!
    No need to strictly follow the template tho. Focus on wit and wow-ing the audience.
    """

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message_content},
        ],
        "temperature": 0.8,  # Increase temperature for more aggressive responses
    }

    cmd = [
        "curl",
        "--header",
        f"Authorization: Bearer {API_KEY}",
        "--header",
        "Content-Type: application/json",
        "--data",
        json.dumps(data),
        "--url",
        URL,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        return extract_content(response)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return None


def record_audio(timed_recording=False, record_seconds=AUDIO_DEFAULT_DURATION):
    """Records audio from the microphone.

    Args:
        timed_recording (bool): If True, record for a fixed duration.
        record_seconds (int): Duration of recording in seconds.

    Returns:
        str: Path to the temporary audio file.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(
        suffix=f".{AUDIO_FORMAT}", dir=TEMP_DIR, delete=False
    )
    temp_file_name = temp_file.name

    def callback(data_input, frame_count, time_info, status):
        wav_file.writeframes(data_input)
        return (None, pyaudio.paContinue)

    with wave.open(temp_file_name, "wb") as wav_file:
        wav_file.setnchannels(AUDIO_CHANNELS)
        wav_file.setsampwidth(2)  # 16-bit samples
        wav_file.setframerate(AUDIO_SAMPLE_RATE)

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=AUDIO_CHANNELS,
            rate=AUDIO_SAMPLE_RATE,
            input=True,
            frames_per_buffer=AUDIO_CHUNK_SIZE,
            stream_callback=callback,
        )

        if timed_recording:
            print(f"Recording for {record_seconds} seconds...")
            time.sleep(record_seconds)
        else:
            input("Press Enter to stop recording...")

        stream.stop_stream()
        stream.close()
        audio.terminate()

    return temp_file_name


def transcribe_audio_file(file_name, prompt=""):
    """Transcribes an audio file using OpenAI's Whisper API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        with open(file_name, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, prompt=prompt
            )
            return response.text.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return None


def translate_audio_file(file_name, prompt=""):
    """Translates an audio file to English using OpenAI's Whisper API."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        with open(file_name, "rb") as audio_file:
            response = client.audio.translations.create(
                model="whisper-1", file=audio_file, prompt=prompt
            )
            return response.text.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def process_audio(
    prompt="",
    timed_recording=False,
    record_seconds=AUDIO_DEFAULT_DURATION,
    is_english=True,
):
    """Records and processes audio, returning transcribed/translated text."""
    temp_file_name = record_audio(timed_recording, record_seconds)

    try:
        if is_english:
            result = transcribe_audio_file(temp_file_name, prompt)
        else:
            result = translate_audio_file(temp_file_name, prompt)

        pyperclip.copy(result)
        return result
    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)


def process_audio_and_chat(
    prompt="Let's debate this topic.",  # Updated default prompt
    timed_recording=False,
    record_seconds=AUDIO_DEFAULT_DURATION,
    is_english=True,
):
    """Records audio, transcribes it, and gets AI response"""
    transcription = process_audio(
        prompt=prompt,
        timed_recording=timed_recording,
        record_seconds=record_seconds,
        is_english=is_english,
    )

    if transcription:
        print("\nYou said:", transcription)
        # Enhance the transcription with debate context
        debate_prompt = f"Debate this point: {transcription}"
        ai_response = send_chat_message(debate_prompt)
        return transcription, ai_response
    return None, None


if __name__ == "__main__":
    # Example usage
    response = send_chat_message("Say this is a test")
    print("AI response:", response)

    # Audio transcription example
    result = process_audio(
        prompt="This is a transcription test.", timed_recording=True, record_seconds=5
    )
    print("Transcription:", result)
