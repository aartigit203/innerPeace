from flask import Flask, request
import requests
import os
from stories import get_story

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


# 📩 SEND MESSAGE FUNCTION
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

    requests.post(url, headers=headers, json=data)


# 🧘 INNER PEACE RESPONSE (KEEP YOUR EXISTING LOGIC HERE)
def get_krishna_response(text, sender):
    # 👉 You can replace this with your GPT / shloka logic
    return f"Hare Krishna 🙏 Reflecting on: {text}"


# 🌐 WEBHOOK
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # 🔐 VERIFY TOKEN
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "error", 403

    # 📩 HANDLE MESSAGE
    data = request.json

    try:
        entry = data["entry"][0]["changes"][0]["value"]

        if "messages" not in entry:
            return "ok", 200

        msg = entry["messages"][0]

        if "text" not in msg:
            return "ok", 200

        sender = msg["from"]
        text = msg["text"]["body"].strip().lower()

        print("User:", text)

        # 🌟 MAIN MENU
        if text in ["hi", "hello", "start"]:
            send_message(sender,
"""Hare Krishna 🙏

Welcome 🌸

Please choose:

1️⃣ Inner Peace (Guidance)
2️⃣ BalGokulam (Kids Stories)""")

        # 🧘 INNER PEACE MODE
        elif text == "1":
            send_message(sender,
"""🧘 Inner Peace 🌸

Ask me anything troubling your mind 💭
Krishna will guide you 🙏""")

        # 👶 BALGOKULAM MENU
        elif text == "2":
            send_message(sender,
"""👶 BalGokulam 🌸

Reply:
1️⃣ Story of the Day
2️⃣ Fun Activity""")

        # 📖 STORY (BalGokulam)
        elif text in ["story", "1️⃣"]:
            send_message(sender, get_story())

        # 🎯 ACTIVITY
        elif text in ["activity", "2️⃣"]:
            send_message(sender,
"""🎯 Activity Time!

Draw Krishna with cows 🐄
OR
Chant Hare Krishna 5 times 🎶""")

        # 🤖 DEFAULT → INNER PEACE
        else:
            reply = get_krishna_response(text, sender)
            send_message(sender, reply)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


# 🚀 RUN APP
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
