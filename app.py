from flask import Flask, render_template, jsonify
from demo_conversation import conversation_demo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_debate', methods=['POST'])
def start_debate():
    try:
        # Will implement WebSocket for real-time later
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
