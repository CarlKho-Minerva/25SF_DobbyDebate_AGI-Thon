from flask import Flask, render_template, request, has_request_context
from flask_socketio import SocketIO
import logging
from services.audio_service import AudioService
from services.chat_service import ChatService
from services.transcription_service import TranscriptionService
import time
import os
from functools import wraps

app = Flask(__name__)
socketio = SocketIO(
    app, cors_allowed_origins="*", async_mode="threading", ping_timeout=60
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize services
audio_service = AudioService()
chat_service = ChatService()
transcription_service = TranscriptionService()


@app.route("/")
def index():
    return render_template("index.html")


def ensure_request_context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not has_request_context():
            with app.request_context():
                return f(*args, **kwargs)
        return f(*args, **kwargs)
    return wrapper

@socketio.on("start_recording")
@ensure_request_context
def handle_recording():
    """Handle recording with improved error handling"""
    temp_file = None
    try:
        current_topic = request.args.get("topic", "Debate this topic")
        logger.info(f"Starting recording for topic: {current_topic}")
        socketio.emit("recording_started")

        # Record audio
        temp_file = audio_service.record_audio(timed_recording=True, record_seconds=5)
        logger.debug(f"Audio recorded to: {temp_file}")

        if not temp_file:
            raise Exception("No audio file was created")
        if not os.path.exists(temp_file):
            raise Exception(f"Audio file not found at: {temp_file}")
        if os.path.getsize(temp_file) == 0:
            raise Exception("Audio file is empty")

        # Transcribe audio
        logger.debug(f"Attempting transcription of: {temp_file}")
        transcription = transcription_service.transcribe(
            temp_file,
            prompt=f"Debate this topic briefly: {current_topic}"
        )
        if not transcription:
            raise Exception("Transcription failed - no text received")
        logger.info(f"Transcription received: {transcription[:50]}...")

        # Get AI response
        ai_response = chat_service.send_message(
            f"Respond to this point briefly: {transcription}"
        )
        if not ai_response:
            raise Exception("No AI response received")
        logger.info(f"AI response received: {ai_response[:50]}...")

        # Emit response
        socketio.emit(
            "dobby_response",
            {
                "text": ai_response,
                "user_said": transcription,
                "timestamp": time.time()
            }
        )

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Recording failed: {error_msg}", exc_info=True)
        socketio.emit("error", {"message": f"Recording failed: {error_msg}"})

    finally:
        # Cleanup temp file
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as e:
                logger.error(f"Failed to remove temp file: {str(e)}")


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
