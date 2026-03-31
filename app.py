rom flask import Flask, request
import requests
import os
import threading
from openai import OpenAI
from shlokas import find_shloka_response

app = Flask(_name_)

# ENV
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

client = OpenAI()

# MEMORY
user_memory = {}
processed_ids = set()


# SEND MESSAGE
def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)


# RESPONSE LOGIC
def get_krishna_response(text, sender):

    # 1️⃣ SHLOKA MATCH
    shloka = find_shloka_response(text)

    if shloka:
        return shloka

    # 2️⃣ GPT FALLBACK
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Krishna guiding with compassion."},
                {"role": "user", "content": text}
            ],
            max_tokens=150
        )

        return "Hare Krishna 🙏\n\n" + res.choices[0].message.content

    except:
        return "Hare Krishna 🙏 Krishna is always with you 💖"


# BACKGROUND RESPONSE
def process_and_reply(sender, text):
    reply = get_krishna_response(text, sender)
    send_message(sender, reply)


# WEBHOOK
@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # VERIFY
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        return "error", 403

    # MESSAGE
    data = request.json

    try:
        entry = data["entry"][0]["changes"][0]["value"]

        if "messages" not in entry:
            return "ok", 200

        msg = entry["messages"][0]
        msg_id = msg.get("id")

        # 🚫 prevent duplicate replies
        if msg_id in processed_ids:
            return "ok", 200

        processed_ids.add(msg_id)

        if "text" not in msg:
            return "ok", 200

        sender = msg["from"]
        text = msg["text"]["body"]

        print("User:", text)

        # ⚡ instant reply
        send_message(sender, "Hare Krishna 🙏 Reflecting...")

        # 🚀 async reply
        threading.Thread(target=process_and_reply, args=(sender, text)).start()

    except Exception as e:
        print("Error:", e)

    return "ok", 200


# RUN
if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



















