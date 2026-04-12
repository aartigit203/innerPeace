import requests, os, json, datetime
from services.daily_stories import get_daily_story
from utils.json_utils import load_json, save_json
from services.whatsapp import send_message, send_buttons
from services.quiz_service import set_quiz, get_quiz
from services.streak_service import update_streak
from services.leaderboard_service import update_score, get_leaderboard
from services.user_service import add_user
from datetime import date

FILE = "data/users_daily.json"


#WHATSAPP_TOKEN = os.getenv("ACCESS_TOKEN")
#PHONE_NUMBER_ID = os.getenv("DAILY_PHONE_NUMBER_ID")

#headers = {
    "Authorization": "Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
        }        


# ---------- LOCK ----------
def already_sent_today(user):
    log = load_json("daily_log.json")
    today = str(datetime.date.today())

    if log.get(user) == today:
        return True

    log[user] = today
    save_json("daily_log.json", log)
    return False

# ---------- SEND ----------

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

    res = requests.post(url, headers=headers, json=payload)
    print("Sending to", to)
    print("STATUS", res.status_code)
    print("RESPONSE", res.text)


def main():

    users = load_json(FILE)
    #users= { "919902244500": {"name": "Aarti"}}
    print("users loaded:",users)

    if not users:
        print("X No Users found")
        exit()
        
    for user, data in user.itmes():
        if not data.get("subscribed"):
            continue

        user_data = users[user]
        day=user_data.get("day",1)
        print("sendingto", user)

        
       # missed = check_missed_users()
        
        #for user in missed:
        
            #msg = """🌸 Hare Krishna 🙏
        
        #Krishna noticed you were not here yesterday 💛
        
        #No worries… come back today 🌿  
        #Every small step towards Him matters ✨"""
        
            #send_message(user, msg)
    
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
        user_data["day"] = day+1
        save_json("data/users_daily.json", users)

        message = f"""🌸 Hare Krishna 🙏

        ✨  Come back tomorrow for next story 💛"""

        send_message(user, message)

        # Send quiz
        send_buttons(user, "🌸 Quiz Time!\nReply A, B or C")
        

        

if __name__ == "__main__":
    main()
