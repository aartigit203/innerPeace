from flask import Flask, request
from services.whatsapp import send_message, send_buttons
from services.quiz_service import set_quiz, get_quiz
from services.streak_service import update_streak
from services.leaderboard_service import update_score, get_leaderboard
from services.user_service import add_user
from stories import get_story
from shlokas import get_shloka_response
import os

app = Flask(__name__)
user_mode = {}
#VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
VERIFY_TOKEN = "krishna123"
print("VEIRFY TOKEN", VERIFY_TOKEN)
@app.route("/webhook", methods=["GET","POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        print("VEIRFY TOKEN", VERIFY_TOKEN)
        
        print(" verify token", verify_token)
        
        if verify_token == VERIFY_TOKEN:
            return challenge
        return "Invalid token", 403

    # POST (actual messages)
    data = request.json
    print("🔥 Webhook HIT", data)

    print("DATA", data)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")

        if not messages:
            return "ok", 200

        msg = messages[0]

        sender = msg["from"]
        text = msg["text"]["body"].lower() if msg["type"] == "text" else ""

        print("Sender:", sender)
        print("Text:", text)

    except Exception as e:
        print("ERROR:", e)
        return "ok", 200


    add_user(sender)

    # MENU
    if text in ["hare krishna","menu"]:
        send_buttons(sender,"🌸 Hare Krishna 🙏",
        [
            {"type":"reply","reply":{"id":"peace","title":"🧘 Peace"}},
            {"type":"reply","reply":{"id":"story","title":"📖 InstantStory"}},
            {"type":"reply","reply":{"id":"dailystory","title":"📖 DailyStory"}},
            {"type":"reply","reply":{"id":"leader","title":"🏆 Leaderboard"}}
        ])
        return "ok",200

    # PEACE
    if text=="peace":
        user_mode[sender]="peace"
        send_message(sender,"🧘 Tell me your thoughts 💭")
        return "ok",200

    if user_mode.get(sender)=="peace":
        send_message(sender,get_shloka_response(text))
        return "ok",200

    # STORY
    if text=="story":
        s = get_story()

        send_message(sender,s["text"])
        
        quiz = s.get("quiz")
        
        if not quiz:
            send_message(sender, "🌸 No quiz today 😊")
            return "ok",200

        set_quiz(sender, quiz["answer"])

        send_buttons(
            sender,
            quiz["question"],
            [
                {"type":"reply","reply":{"id":"a","title":quiz["options"]["a"]}},
                {"type":"reply","reply":{"id":"b","title":quiz["options"]["b"]}},
                {"type":"reply","reply":{"id":"c","title":quiz["options"]["c"]}}
            ]
            )

    #return "ok",200


    # ANSWER
        if text in ["a","b","c"]:
            correct = get_quiz(sender)

        if not correct:
            send_message(sender,"⚠️ Try story again")
            return "ok",200

        streak = update_streak(sender)

        if text == correct:
            update_score(sender)
            send_message(sender,f"🎉 Correct!\n🔥 Streak: {streak}")
        else:
            send_message(sender,f"😊 Correct answer: {correct.upper()}")

        return "ok",200

    # LEADERBOARD
    if text=="leader":
        top = get_leaderboard()

        if not top:
            send_message(sender,"🌸 No scores yet")
            return "ok",200

        msg="🏆 Leaderboard\n\n"
        for i,(u,s) in enumerate(top[:5],1):
            msg += f"{i}. {u[-4:]} → {s} 🔥\n"

        send_message(sender,msg)
        return "ok",200

    return "ok",200

    #DailyStory
    if text == "dailystory":

        users = load_json("data/users_daily.json")

        if sender not in users:
            users[sender] = {
                "name": "User",
                "day": 1,
                "subscribed": True
                }
            save_json("data/users_daily.json", users)

            send_message(sender,
            "🌸 You are now registered for Daily Krishna Stories!\n\nYou will receive stories every evening 😊")

        else:
            send_message(sender,
            "🌸 You are already subscribed, will recieve daily story at 11:00 AM IST 😊")

    return "ok", 200


app.run(host="0.0.0.0",port=10000)
