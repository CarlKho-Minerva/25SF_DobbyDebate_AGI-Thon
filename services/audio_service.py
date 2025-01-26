import os
import wave
import tempfile
import pyaudio
from typing import Optional
from config import AudioConfig


class AudioService:
    def __init__(self, config: AudioConfig):
        self.config = config

    def record_audio(
        self, timed_recording: bool = False, record_seconds: int = 5
    ) -> Optional[str]:
        """Records audio and returns path to temporary file"""
        os.makedirs(self.config.temp_dir, exist_ok=True)
        temp_file = tempfile.NamedTemporaryFile(
            suffix=f".{self.config.format}", dir=self.config.temp_dir, delete=False
        )
        temp_file_name = temp_file.name

        with wave.open(temp_file_name, "wb") as wav_file:
            wav_file.setnchannels(self.config.channels)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.config.sample_rate)

            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=self.config.channels,
                rate=self.config.sample_rate,
                input=True,
                frames_per_buffer=self.config.chunk_size,
            )

            frames = []
            try:
                if timed_recording:
                    for _ in range(
                        0,
                        int(
                            self.config.sample_rate
                            / self.config.chunk_size
                            * record_seconds
                        ),
                    ):
                        data = stream.read(self.config.chunk_size)
                        frames.append(data)
                else:
                    while True:
                        data = stream.read(self.config.chunk_size)
                        frames.append(data)
            finally:
                stream.stop_stream()
                stream.close()
                audio.terminate()

            for frame in frames:
                wav_file.writeframes(frame)

        return temp_file_name
