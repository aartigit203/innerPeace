import requests, os
from utils.json_utils import load_json, save_json

TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_NUMBER_ID")

# ---------- DEDUPE ----------
def is_duplicate(msg_id):
    data = load_json("processed.json")

    if msg_id in data:
        return True

    data[msg_id] = True
    # Keep only last 1000 message IDs to prevent unbounded growth
    if len(data) > 1000:
        keys = list(data.keys())
        for old_key in keys[:len(data) - 1000]:
            del data[old_key]

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
    try:
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print(f"send_message failed {res.status_code}: {res.text}", flush=True)
    except requests.RequestException as e:
        print(f"send_message error: {e}", flush=True)


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
    try:
        res = requests.post(url, headers=headers, json=payload)
        if not res.ok:
            print(f"send_buttons failed {res.status_code}: {res.text}", flush=True)
    except requests.RequestException as e:
        print(f"send_buttons error: {e}", flush=True)
