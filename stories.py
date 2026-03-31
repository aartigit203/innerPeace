from flask import Flask, request
import requests
import os
from stories import get_story

app = Flask(__name__)

# 🔐 ENV VARIABLES
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# 🧠 USER MODE MEMORY
user_mode = {}   # { phone_number: "innerpeace" or "balgokulam" }


# =========================
# 📩 SEND TEXT MESSAGE
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
        print("Text send error:", e)


# =========================
# 🖼️ SEND IMAGE
# =========================
def send_image(to, image_url, caption=""):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }

    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except Exception as e:
        print("Image send error:", e)


# =========================
# 🎧 SEND AUDIO
# =========================
def send_audio(to, audio_url):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "audio",
        "audio": {
            "link": audio_url
        }
    }

    try:
        requests.post(url, headers=headers, json=data, timeout=5)
    except Exception as e:
        print("Audio send error:", e)


# =========================
# 🧘 INNER PEACE RESPONSE
# =========================
def get_krishna_response(text, sender):
    return f"Hare Krishna 🙏 Reflecting on: {text}"


# =========================
# 🌐 WEBHOOK
# =========================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # 🔐 VERIFY TOKEN
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

        if "text" not in msg:
            return "ok", 200

        sender = msg["from"]
        text = msg["text"]["body"].strip().lower()

        print("User:", sender, text)

        # =========================
        # 🌟 MAIN MENU
        # =========================
        if text in ["hi", "hello", "start", "menu"]:
            user_mode[sender] = None

            send_message(sender,
"""Hare Krishna 🙏

Welcome 🌸

Please choose:

1️⃣ Inner Peace (Guidance)
2️⃣ BalGokulam (Kids Stories)""")

            return "ok", 200

        # =========================
        # 🧘 SELECT INNER PEACE
        # =========================
        if text == "1" and user_mode.get(sender) is None:
            user_mode[sender] = "innerpeace"

            send_message(sender,
"""🧘 Inner Peace 🌸

Ask me anything troubling your mind 💭
Krishna will guide you 🙏""")

            return "ok", 200

        # =========================
        # 👶 SELECT BALGOKULAM
        # =========================
        if text == "2" and user_mode.get(sender) is None:
            user_mode[sender] = "balgokulam"

            send_message(sender,
"""👶 BalGokulam 🌸

Reply:
1️⃣ Story of the Day
2️⃣ Fun Activity

Type 'menu' anytime to go back""")

            return "ok", 200

        # =========================
        # 👶 BALGOKULAM FLOW
        # =========================
        if user_mode.get(sender) == "balgokulam":

            if text in ["1", "story", "1️⃣"]:
                story = get_story()

                # 🖼️ IMAGE
                if isinstance(story, dict) and story.get("image"):
                    send_image(sender, story["image"], story.get("title", ""))

                # 📖 TEXT
                if isinstance(story, dict):
                    send_message(sender, story.get("text", ""))
                else:
                    send_message(sender, story)

                # 🎧 AUDIO
                if isinstance(story, dict) and story.get("audio"):
                    send_audio(sender, story["audio"])

            elif text in ["2", "activity", "2️⃣"]:
                send_message(sender,
"""🎯 Activity Time!

Draw Krishna with cows 🐄
OR
Chant Hare Krishna 5 times 🎶""")

            else:
                send_message(sender,
"""👶 BalGokulam 🌸

Reply:
1️⃣ Story
2️⃣ Activity

Type 'menu' to switch mode""")

            return "ok", 200

        # =========================
        # 🧘 INNER PEACE FLOW
        # =========================
        if user_mode.get(sender) == "innerpeace":
            reply = get_krishna_response(text, sender)
            send_message(sender, reply)
            return "ok", 200

        # =========================
        # 🔄 FALLBACK
        # =========================
        send_message(sender,
"""Hare Krishna 🙏

Type 'hi' to begin 🌸""")

    except Exception as e:
        print("Webhook Error:", e)

    return "ok", 200


# =========================
# 🚀 RUN APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
