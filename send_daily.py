import requests, os, json
from daily_stories import get_daily_story
from datetime import date

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

def send_buttons(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": text},
            "action": {
                "buttons": [
                    {"type":"reply","reply":{"id":"a","title":"A"}},
                    {"type":"reply","reply":{"id":"b","title":"B"}},
                    {"type":"reply","reply":{"id":"c","title":"C"}}
                ]
            }
        }
    }
    requests.post(url, headers=headers, json=payload)

def main():

    users = load_json("users.json")

    for user in users:

        day = users[user]
        story = get_daily_story(day)

        message = f"""🌸 Hare Krishna 🙏

📖 {story['title']}

{story['text']}

🎥 Watch:
{story['video']}

✨ Come back tomorrow for next story 💛"""

        send_message(user, message)

        # Send quiz
        send_buttons(user, "🌸 Quiz Time!\nReply A, B or C")

if __name__ == "__main__":
    main()
