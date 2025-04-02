import tweepy
import requests
import time
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials from .env
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Setup Twitter client
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Backend endpoint
ANALYZE_URL = "http://127.0.0.1:8000/analyze"
BOT_USERNAME = "AskNyai"  # without @

# Logging and checkpoint files
LOG_FILE = "logs/twitter_bot.log"
CHECKPOINT_FILE = "logs/twitter_checkpoint.json"
os.makedirs("logs", exist_ok=True)

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{time.ctime()}] {message}\n")

def save_checkpoint(since_id):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"since_id": since_id}, f)

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f).get("since_id", 1)
    return 1

def process_mention(tweet):
    try:
        user = tweet.user.screen_name
        query = tweet.text.replace(f"@{BOT_USERNAME}", "").strip()
        log(f"New mention from @{user}: {query}")

        payload = {
            "platform": "twitter",
            "user": user,
            "message": query
        }

        res = requests.post(ANALYZE_URL, json=payload, timeout=10)
        res.raise_for_status()
        reply = res.json().get("reply", "Sorry, couldn't process your request.")
        log(f"Replying to @{user} with: {reply}")

        api.update_status(
            status=f"@{user} {reply}",
            in_reply_to_status_id=tweet.id
        )

    except Exception as e:
        log(f"❌ Error processing mention: {str(e)}")

if __name__ == "__main__":
    log("🚀 Twitter bot started")
    since_id = load_checkpoint()

    while True:
        try:
            mentions = api.mentions_timeline(since_id=since_id, tweet_mode='extended')
            for tweet in reversed(mentions):
                process_mention(tweet)
                since_id = max(tweet.id, since_id)
                save_checkpoint(since_id)

        except Exception as e:
            log(f"💥 Error fetching mentions: {str(e)}")

        time.sleep(5)
