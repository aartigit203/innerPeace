from flask import Flask, request
import requests
import urllib.parse
from shlokas import SHLOKAS
import os
import threading
from dotenv import load_dotenv

load_dotenv()
from openai import OpenAI
client = OpenAI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

if not all([VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUMBER_ID]):
    raise ValueError("❌ Missing environment variables. Check .env or export.")




app = Flask(__name__)


processed_ids = set()
response_cache = {}
user_memory = {}

def is_simple_emotion(text):
    text = text.lower()

    keywords = [
        "sad", "happy", "anxious", "stress", "worried",
        "confused", "depressed", "angry", "fear", "tension"
    ]

    return any(word in text for word in keywords)

# 🌿 Normalize text
def normalize(text):
    return text.lower().strip()


# 🧘 Mantra
def get_mantra():
    return """🧘 Chant slowly:

Hare Krishna Hare Krishna Krishna Krishna Hare Hare  
Hare Rama Hare Rama Rama Rama Hare Hare  

Krishna is always with you 🌸"""


# 🚀 GPT response with cache
def get_gpt_response(user_text):
    key = user_text.lower().strip()
    if key in response_cache:
        return response_cache[key]

    try:
        prompt = f"""
User: {user_text}

Give:
- 1 Bhagavad Gita or Srimad Bhagavatam shloka
- Sanskrit
- Simple translation
- 2 line explanation
- Vedabase link (https://www.vedabase.io/...)

Keep it short and compassionate.
"""

        res = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = res.choices[0].message.content

        response_cache[key] = answer  # cache
        return answer

    except Exception as e:
        print("GPT error:", e)
        return get_vedabase_fallback(user_text)
    
def get_vedabase_fallback(user_text):
    query = urllib.parse.quote(user_text)

    return f"""Hare Krishna 🙏

Krishna’s wisdom is available here:

📖 https://www.vedabase.io/en/search/{query}/

🌸 Please explore peacefully."""



# 🌸 Hybrid router
def get_response(text, sender):
    text = normalize(text)

    # Greeting
    if text in ["hi", "hello", "hey"]:
        return "Hare Krishna 🙏 How can I guide you today?"

    # Mantra
    if text == "1":
        return get_mantra()

    # Static fast responses
    for s in SHLOKAS:
        if any(tag in text for tag in s["tags"]):
            user_memory[sender] = s["tags"][0]

            return f"""Hare Krishna 🙏

Krishna says in {s['ref']}:

{s['sanskrit']}

📖 {s['translation']}

🌸 {s['message']}

Reply 1 for calming mantra 🧘"""

    # GPT dynamic
    return get_gpt_response(text)


# 📤 Send WhatsApp message
def send_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": str(message)}
    }

    response = requests.post(url, headers=headers, json=data)
    print("Send:", response.text)


# 🌐 Webhook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verification
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "error", 403

    # Messages
    data = request.json

    try:
        entry = data["entry"][0]["changes"][0]["value"]

        if "messages" in entry:
            msg = entry["messages"][0]

            msg_id = msg.get("id")

            # ✅ Prevent duplicates
            if msg_id in processed_ids:
                return "ok", 200

            processed_ids.add(msg_id)

            if msg.get("type") == "text":
                sender = msg["from"]
                text = msg["text"]["body"]

                print("User:", text)

                # ⚡ Instant reply
                send_message(sender, "Hare Krishna 🙏\n\nLet me reflect on this for you 🌸...")
                # 🚀 Background processing
                def process_and_reply():
                    reply = get_response(text, sender)
                    send_message(sender, reply)
                    # ⚡ Smart handling
                if is_simple_emotion(text):
                    # Fast path (no delay)
                    reply = get_response(text, sender)
                    send_message(sender, reply)
                else:
                    # Slow path (GPT)
                    send_message(sender, "Hare Krishna 🙏\n\nLet me reflect on this for you 🌸...")


                    threading.Thread(target=process_and_reply).start()
                

    except Exception as e:
        print("Error:", e)

    return "ok", 200
    
if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

#if __name__ == "__main__":
    #app.run(port=5010)
