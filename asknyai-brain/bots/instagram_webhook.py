from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
VERIFY_TOKEN = os.getenv("IG_VERIFY_TOKEN")
ANALYZE_URL = "http://127.0.0.1:8000/analyze"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def receive_dm():
    data = request.json

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event["sender"]["id"]
            message_text = event.get("message", {}).get("text", "")

            if "@AskNyai" in message_text:
                query = message_text.replace("@AskNyai", "").strip()
                payload = {
                    "platform": "instagram",
                    "user": sender_id,
                    "message": query
                }
                result = requests.post(ANALYZE_URL, json=payload).json()
                reply = result.get("reply", "Sorry, something went wrong.")

                # TODO: Send reply back using Meta Graph API call here (requires access token + page ID)

    return "ok", 200

if __name__ == "__main__":
    app.run(port=5002)
