from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from Dobby_Class import process_audio_and_chat
from dobby_voice import text_to_speech, play
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def send_audio_to_client(audio_data):
    socketio.emit('dobby_speaking', {'audio': audio_data})

@socketio.on('start_recording')
def handle_recording():
    # Start 5-second timer
    for i in range(5, 0, -1):
        socketio.emit('timer_update', {'seconds': i})
        time.sleep(1)

    transcription, ai_response = process_audio_and_chat(
        prompt="Conversation with user",
        timed_recording=True,
        record_seconds=5,
        is_english=True
    )

    if transcription and ai_response:
        # Convert AI response to speech
        audio = text_to_speech(ai_response)
        if audio:
            socketio.emit('dobby_response', {
                'text': ai_response,
                'user_said': transcription
            })
            # Play audio in background
            threading.Thread(target=play, args=(audio,)).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
