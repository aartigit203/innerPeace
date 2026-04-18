import requests, os, json
from datetime import date
from services.daily_stories import get_daily_story
from utils.json_utils import load_json, save_json
from services.whatsapp import send_message

TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("DAILY_PHONE_NUMBER_ID")


def already_sent_today(user):
    log = load_json("daily_log.json")
    today = str(date.today())

    if log.get(user) == today:
        return True

    log[user] = today
    save_json("daily_log.json", log)
    return False


def send_template(to, day, title, text, video, streak):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "daily_krishna_story",
            "language": {"code": "en"},
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

    try:
        res = requests.post(url, headers=headers, json=payload)
        print("Sending to", to)
        print("STATUS", res.status_code)
        print("RESPONSE", res.text)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send template to {to}: {e}", flush=True)


def main():
    FILE = "data/users_daily.json"
    users = load_json(FILE)
    print("users loaded:", users)

    if not users:
        print("X No Users found")
        return

    for user, data in users.items():
        if not data.get("subscribed"):
            continue

        if already_sent_today(user):
            print(f"Already sent to {user} today, skipping")
            continue

        user_data = users[user]
        day = user_data.get("day", 1)
        print("sending to", user)

        story = get_daily_story(day)
        streak_data = load_json("data/streak.json")
        streak = streak_data.get(user, {}).get("count", 1)

        send_template(
            user,
            story["day"],
            story["title"],
            story["text"],
            story["video"],
            streak
        )

        print("story", story["text"])
        user_data["day"] = day + 1
        save_json(FILE, users)

        message = "🌸 Hare Krishna 🙏\n\n✨ Come back tomorrow for next story 💛"
        send_message(user, message)


if __name__ == "__main__":
    main()
