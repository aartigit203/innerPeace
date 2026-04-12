import requests, os, json
from services.daily_stories import get_daily_story
from services.user_service import check_missed_users
from datetime import date

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("DAILY_PHONE_NUMBER_ID")

headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

def load_json(file):
    try:
        with open(file) as f:
            print("JSON Loaded",json.dump(f))
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def send_template(to, day, title, text, video, streak):

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    print("to",to)
    print("text", text)

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "daily_krishna_story",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": str(day)},
                        {"type": "text", "text": title},
                        {"type": "text", "text": text[:500]},
                        {"type": "text", "text": video},
                        {"type": "text", "text": str(streak)}
                    ]
                }
            ]
        }
    }

    res = requests.post(url, headers=headers, json=payload)
    print("Sending to", to)
    print("STATUS", res.status_code)
    print("RESPONSE", res.text)

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

    users = load_json("users_daily.json")
    users= { "919902244500": {"name": "Aarti"}
            }
    print("users loaded:",users)

    if not users:
        print("X No Users found")
        exit()
        
    for user in users:

        day = users[user]
        print("sendingto", user)

        
        missed = check_missed_users()
        
        for user in missed:
        
            msg = """🌸 Hare Krishna 🙏
        
        Krishna noticed you were not here yesterday 💛
        
        No worries… come back today 🌿  
        Every small step towards Him matters ✨"""
        
            send_message(user, msg)
    
        story = get_daily_story(day)
        streak_data = load_json("streak.json")
        streak = streak_data.get(user, {}).get("count", 1)

        send_template(
        user,
        story["day"],
        story["title"],
        story["text"],
        story["video"],
        streak
        )

        print("story",story["text"])

        message = f"""🌸 Hare Krishna 🙏

        ✨  Come back tomorrow for next story 💛"""

        send_message(user, message)

        # Send quiz
        send_buttons(user, "🌸 Quiz Time!\nReply A, B or C")

        

if __name__ == "__main__":
    main()
