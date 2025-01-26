import os
import wave
import tempfile
import pyaudio
from typing import Optional
from config import SAMPLE_RATE, CHANNELS, CHUNK_SIZE, FORMAT, TEMP_DIR, RECORD_SECONDS, ELEVENLABS_API_KEY


class AudioService:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.channels = CHANNELS
        self.chunk_size = CHUNK_SIZE
        self.format = FORMAT
        self.temp_dir = TEMP_DIR
        self.record_seconds = RECORD_SECONDS
        self.api_key = ELEVENLABS_API_KEY

        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def record_audio(
        self, timed_recording: bool = False, record_seconds: int = 5
    ) -> Optional[str]:
        """Records audio and returns path to temporary file"""
        os.makedirs(self.temp_dir, exist_ok=True)
        temp_file = tempfile.NamedTemporaryFile(
            suffix=f".{self.format}", dir=self.temp_dir, delete=False
        )
        temp_file_name = temp_file.name

        with wave.open(temp_file_name, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)

            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
            )

            frames = []
            try:
                if timed_recording:
                    for _ in range(
                        0,
                        int(
                            self.sample_rate
                            / self.chunk_size
                            * record_seconds
                        ),
                    ):
                        data = stream.read(self.chunk_size)
                        frames.append(data)
                else:
                    while True:
                        data = stream.read(self.chunk_size)
                        frames.append(data)
            finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()

            for frame in frames:
                wav_file.writeframes(frame)

        return temp_file_name
