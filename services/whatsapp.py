import requests, os, json, datetime
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")

# ---------- HELPERS ----------
def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# ---------- DEDUPE ----------
def is_duplicate(msg_id):
    data = load_json("processed.json")

    if msg_id in data:
        return True

    data[msg_id] = True
    save_json("processed.json", data)
    return False

# ---------- SEND ----------
def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    requests.post(url, headers=headers, json=payload)

def send_buttons(to, text, buttons):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {"buttons": buttons}
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("META Response", response.text, flush=True)

 
