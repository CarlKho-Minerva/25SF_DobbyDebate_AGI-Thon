from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from Dobby_Class import process_audio_and_chat
from dobby_voice import text_to_speech, play
import threading
import time
from typing import Optional
import logging
from functools import wraps

# Initialize Flask
app = Flask(__name__)

# Configure SocketIO with threading mode
socketio = SocketIO(
    app, cors_allowed_origins="*", async_mode="threading", ping_timeout=60
)

logger = logging.getLogger(__name__)
app.config['JSON_SORT_KEYS'] = False  # Preserve response order

def async_handler(f):
    """Decorator for handling async operations"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        def task():
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in async task: {str(e)}")
                socketio.emit("error", {"message": "Internal server error"})
        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()
        return thread
    return wrapped

def emit_timer(seconds: int) -> None:
    """Emit timer updates"""
    for i in range(seconds, 0, -1):
        socketio.emit("timer_update", {"seconds": i})
        time.sleep(1)
    socketio.emit("timer_update", {"seconds": 0})

def debug_log(msg_type: str, message: str, data: dict = None) -> None:
    """Enhanced debug logging"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {msg_type}: {message}"
    if data:
        log_msg += f"\nData: {data}"
    logger.info(log_msg)

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("start_recording")
def handle_recording():
    """Handle recording with optimized response flow"""
    try:
        current_topic = request.args.get('topic', 'Debate this topic')
        debug_log("INFO", "Starting recording session", {"topic": current_topic})
        socketio.emit("recording_started")

        # Process audio and get response
        transcription, ai_response = process_audio_and_chat(
            prompt=f"Debate this topic briefly: {current_topic}",
            timed_recording=True,
            record_seconds=5,
            is_english=True,
        )

        if transcription and ai_response:
            debug_log("INFO", "Got response", {
                "transcription_length": len(transcription),
                "response_length": len(ai_response)
            })
            audio = text_to_speech(ai_response)
            if audio:
                socketio.emit(
                    "dobby_response",
                    {
                        "text": ai_response,
                        "user_said": transcription,
                        "timestamp": time.time()
                    }
                )
                play(audio)
        else:
            debug_log("ERROR", "No response generated")

    except Exception as e:
        debug_log("ERROR", f"Recording failed: {str(e)}")
        socketio.emit("error", {"message": "Recording failed"})

if __name__ == "__main__":
    try:
        print("Starting server...")
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"Server error: {e}")
