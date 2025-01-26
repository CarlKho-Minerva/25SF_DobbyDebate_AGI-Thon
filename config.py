# If env is not found, please hardcode the values here
API_KEY = ""  # Fireworks AI for Dobby
OPENAI_API_KEY = ""
ELEVENLABS_API_KEY = ""


URL = "https://api.fireworks.ai/inference/v1/chat/completions"
MODEL = "accounts/sentientfoundation/models/dobby-mini-unhinged-llama-3-1-8b#accounts/sentientfoundation/deployments/81e155fc"

# Audio settings
TEMP_DIR = "temp"
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_CHUNK_SIZE = 1024
AUDIO_FORMAT = "wav"
AUDIO_DEFAULT_DURATION = 5  # seconds
