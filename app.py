from flask import Flask, request
import requests
import os
import json

from shlokas import get_shloka_response
from stories import get_story

# 🧠 AI
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# =========================
# 💾 PERSISTENT MEMORY
# =========================
MEMORY_FILE = "user_memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

user_mode = load_memory()
processed_messages = set()


# =========================
# 📩 SEND TEXT
# =========================
def send_message(to, msg):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": msg}
    }
    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except Exception as e:
        print("Text error:", e)


# =========================
# 🖼️ IMAGE
# =========================
def send_image(to, img, caption=""):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {"link": img, "caption": caption}
    }
    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except Exception as e:
        print("Image error:", e)


# =========================
# 🎧 AUDIO
# =========================
def send_audio(to, audio):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": {"link": audio}
    }
    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except Exception as e:
        print("Audio error:", e)


# =========================
# 🧘 AI KRISHNA RESPONSE
# =========================
def get_ai_response(user_text):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are Lord Krishna giving calm, spiritual, Bhagavad Gita based guidance in simple words."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            max_tokens=200
        )

        return "Hare Krishna 🙏\n\n" + response.choices[0].message.content

    except Exception as e:
        print("AI error:", e)

        # fallback
        return get_shloka_response(user_text)


# =========================
# 🌐 WEBHOOK
# =========================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "error", 403

    data = request.json

    try:
        entry = data["entry"][0]["changes"][0]["value"]

        if "messages" not in entry:
            return "ok", 200

        msg = entry["messages"][0]

        # 🚫 DUPLICATE FIX
        msg_id = msg.get("id")
        if msg_id in processed_messages:
            return "ok", 200
        processed_messages.add(msg_id)

        if "text" not in msg:
            return "ok", 200

        sender = msg["from"]
        text = msg["text"]["body"].strip().lower()

        print(sender, text)

        # =========================
        # MENU
        # =========================
        if text in ["hi", "hello", "start", "menu"]:
            user_mode[sender] = None
            save_memory(user_mode)

            send_message(sender,
"""Hare Krishna 🙏

Please choose:

1️⃣ Inner Peace (Guidance)
2️⃣ BalGokulam (Kids Stories)""")

            return "ok", 200

        # =========================
        # SELECT MODES
        # =========================
        if text == "1" and user_mode.get(sender) is None:
            user_mode[sender] = "innerpeace"
            save_memory(user_mode)

            send_message(sender,
"""🧘 Inner Peace 🌸

Share what is troubling your mind 💭""")

            return "ok", 200

        if text == "2" and user_mode.get(sender) is None:
            user_mode[sender] = "balgokulam"
            save_memory(user_mode)

            send_message(sender,
"""👶 BalGokulam 🌸

Reply:
1️⃣ Story
2️⃣ Activity""")

            return "ok", 200

        # =========================
        # BALGOKULAM
        # =========================
        if user_mode.get(sender) == "balgokulam":

            if text in ["1", "story"]:
                story = get_story()

                if story.get("image"):
                    send_image(sender, story["image"], story["title"])

                send_message(sender, story["text"])

                if story.get("audio"):
                    send_audio(sender, story["audio"])

                if story.get("quiz"):
                    send_message(sender, story["quiz"])

            elif text in ["2", "activity"]:
                send_message(sender,
"""🎯 Activity Time!

Draw Krishna OR chant 5 times 🙏""")

            return "ok", 200

        # =========================
        # INNER PEACE (AI + SHLOKA)
        # =========================
        if user_mode.get(sender) == "innerpeace":

            reply = get_ai_response(text)
            send_message(sender, reply)

            return "ok", 200

    except Exception as e:
        print("Error:", e)

    return "ok", 200


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
