from flask import Flask, request
import requests
import os
import json
import threading
import time
from datetime import datetime

from shlokas import get_shloka_response
from stories import get_story

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# =========================
# MEMORY FILES
# =========================
MEMORY_FILE = "user_memory.json"
USERS_FILE = "users.json"

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

user_mode = load_json(MEMORY_FILE)
user_quiz = {}
user_streak = {}
processed_messages = set()

def save_user(num):
    users = load_json(USERS_FILE)
    if num not in users:
        users.append(num)
        save_json(USERS_FILE, users)

# =========================
# SEND FUNCTIONS
# =========================
def send_message(to, msg):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp","to": to,"type": "text","text": {"body": msg}}
    requests.post(url, headers=headers, json=data)

def send_buttons(to, body, buttons):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {"type": "button","body": {"text": body},"action": {"buttons": buttons}}
    }
    requests.post(url, headers=headers, json=data)

def send_image(to, img, caption=""):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp","to": to,"type": "image","image": {"link": img,"caption": caption}}
    requests.post(url, headers=headers, json=data)

def send_audio(to, audio):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp","to": to,"type": "audio","audio": {"link": audio}}
    requests.post(url, headers=headers, json=data)

# =========================
# AI RESPONSE
# =========================
def get_ai_response(text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Krishna giving calm Bhagavad Gita based guidance."},
                {"role": "user", "content": text}
            ]
        )
        return "🌸 Hare Krishna 🙏\n\n" + res.choices[0].message.content
    except:
        return get_shloka_response(text)

# =========================
# DAILY BROADCAST
# =========================
def daily_broadcast():
    while True:
        now = datetime.now()
        if now.hour == 7 and now.minute == 0:
            users = load_json(USERS_FILE)
            story = get_story()
            for u in users:
                send_message(u, f"🌅 Good Morning 🌸\n\n{story['text'][:300]}")
            time.sleep(60)
        time.sleep(20)

threading.Thread(target=daily_broadcast, daemon=True).start()

# =========================
# WEBHOOK
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

        msg_id = msg.get("id")
        if msg_id in processed_messages:
            return "ok", 200
        processed_messages.add(msg_id)

        sender = msg["from"]
        save_user(sender)

        if "interactive" in msg:
            text = msg["interactive"]["button_reply"]["id"]
        else:
            text = msg["text"]["body"].lower().strip()

        # ================= MENU =================
        if text in ["hi", "menu", "start"]:
            user_mode[sender] = None
            save_json(MEMORY_FILE, user_mode)

            send_buttons(sender,
                "🌸 Hare Krishna 🙏\n\nWelcome ✨\n\nWhat would you like?",
                [
                    {"type": "reply","reply": {"id": "inner","title": "🧘 Inner Peace"}},
                    {"type": "reply","reply": {"id": "bal","title": "👶 Balgokulam"}}
                ])
            return "ok", 200

        # ================= SELECT =================
        if text in ["inner","1"] and user_mode.get(sender) is None:
            user_mode[sender] = "innerpeace"
            save_json(MEMORY_FILE, user_mode)
            send_message(sender, "🧘 Share your thoughts 💭")
            return "ok", 200

        if text in ["bal","2"] and user_mode.get(sender) is None:
            user_mode[sender] = "balgokulam"
            save_json(MEMORY_FILE, user_mode)

            send_buttons(sender,
                "👶 BalGokulam 🌸",
                [
                    {"type": "reply","reply": {"id": "story","title": "📖 Story"}},
                    {"type": "reply","reply": {"id": "activity","title": "🎯 Activity"}}
                ])
            return "ok", 200

        # ================= QUIZ =================
        if sender in user_quiz and text.startswith("opt_"):

            correct = user_quiz[sender]["answer"]

            if text == correct:
                send_buttons(sender,
                    "🌸 Correct! Krishna is happy 💛",
                    [
                        {"type": "reply","reply": {"id": "next","title": "➡️ Next Story"}},
                        {"type": "reply","reply": {"id": "menu","title": "🏠 Menu"}}
                    ])
            else:
                send_buttons(sender,
                    f"💛 Correct answer: {correct}",
                    [
                        {"type": "reply","reply": {"id": "next","title": "➡️ Try Another"}},
                        {"type": "reply","reply": {"id": "menu","title": "🏠 Menu"}}
                    ])

            del user_quiz[sender]
            return "ok", 200

        # ================= BALGOKULAM =================
        if user_mode.get(sender) == "balgokulam":

            if text in ["story","next"]:
                story = get_story()

                send_image(sender, story["image"], story["title"])
                send_message(sender, story["text"])

                send_buttons(sender,
                    story["quiz_question"],
                    [{"type":"reply","reply": opt} for opt in story["quiz_options"]]
                )

                user_quiz[sender] = {"answer": story["answer"]}

            elif text == "activity":
                send_message(sender, "🎯 Draw Krishna or chant 5 times 🙏")

            return "ok", 200

        # ================= INNER PEACE =================
        if user_mode.get(sender) == "innerpeace":
            send_message(sender, get_ai_response(text))
            return "ok", 200

    except Exception as e:
        print("Error:", e)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
