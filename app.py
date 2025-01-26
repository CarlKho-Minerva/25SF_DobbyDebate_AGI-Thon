from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from Dobby_Class import process_audio_and_chat
from dobby_voice import text_to_speech, play
import threading
import time

# Initialize Flask
app = Flask(__name__)

# Configure SocketIO with threading mode
socketio = SocketIO(
    app, cors_allowed_origins="*", async_mode="threading", ping_timeout=60
)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("start_recording")
def handle_recording():
    try:
        current_topic = request.args.get('topic', 'Debate this topic')
        socketio.emit("recording_started", {"status": "started"})

        # Start timer in background thread
        def timer_thread():
            for i in range(5, 0, -1):
                socketio.emit("timer_update", {"seconds": i})
                time.sleep(1)
            socketio.emit("timer_update", {"seconds": 0})

        timer = threading.Thread(target=timer_thread)
        timer.daemon = True
        timer.start()

        # Process audio in main thread
        transcription, ai_response = process_audio_and_chat(
            prompt=f"Debate this topic: {current_topic}",
            timed_recording=True,
            record_seconds=5,
            is_english=True,
        )

        if transcription and ai_response:
            # Convert AI response to speech
            audio = text_to_speech(ai_response)
            if audio:
                socketio.emit(
                    "dobby_response", {"text": ai_response, "user_said": transcription}
                )
                # Play audio in background
                player = threading.Thread(target=play, args=(audio,))
                player.daemon = True
                player.start()

    except Exception as e:
        print(f"Error in handle_recording: {e}")
        socketio.emit("error", {"message": str(e)})


if __name__ == "__main__":
    try:
        print("Starting server...")
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"Server error: {e}")
