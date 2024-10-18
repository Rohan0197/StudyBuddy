from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gradio_client import Client, handle_file
import logging
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Gradio client setup
client = Client("http://localhost:8001/")

# Logging setup
logging.basicConfig(level=logging.INFO)

# Root route to serve the HTML file
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"message": "GET method is not allowed. Please use POST to interact with the chatbot."}), 405

    if request.method == 'POST':
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data.get('message')
        logging.info(f"Received message: {user_message}")

        try:
            result = client.predict(
                message=user_message,
                mode="RAG",
                param_3=None,
                param_4=user_message,
                api_name="/chat"
            )
            logging.info(f"Gradio response: {result}")
            return jsonify({"response": result})

        except Exception as e:
            logging.error(f"Error: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
