from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)

ANALYZE_URL = "http://127.0.0.1:8000/analyze"
LOG_FILE = "logs/interactions.txt"

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_interaction(sender, question, reply):
    """Logs the conversation to a file for debugging and traceability."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {sender} asked: {question}\n")
        log_file.write(f"[{timestamp}] Reply: {reply}\n\n")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "unknown")

    if "@AskNyai" in incoming_msg:
        query = incoming_msg.replace("@AskNyai", "").strip()

        payload = {
            "platform": "whatsapp",
            "user": sender,
            "message": query
        }

        try:
            response = requests.post(ANALYZE_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            reply = data.get("reply", "Sorry, I couldn't understand that.")
        except Exception as e:
            reply = "Sorry, something went wrong while processing your request."
            log_interaction(sender, query, f"ERROR: {str(e)}")
        else:
            log_interaction(sender, query, reply)
    else:
        reply = "Send a legal question using @AskNyai to get help."
        log_interaction(sender, incoming_msg, reply)

    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
