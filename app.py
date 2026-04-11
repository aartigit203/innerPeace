from flask import Flask, request
from services.whatsapp import send_message, send_buttons
from services.quiz_service import set_quiz, get_quiz
from services.streak_service import update_streak
from services.leaderboard_service import update_score, get_leaderboard
from services.user_service import add_user
from stories import get_story
from shlokas import get_shloka_response

app = Flask(__name__)
user_mode = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = msg["from"]
        text = msg["text"]["body"].lower() if msg["type"]=="text" else msg["interactive"]["button_reply"]["id"]
    except:
        return "ok",200

    add_user(sender)

    # MENU
    if text in ["hi","menu"]:
        send_buttons(sender,"🌸 Hare Krishna 🙏",
        [
            {"type":"reply","reply":{"id":"peace","title":"🧘 Peace"}},
            {"type":"reply","reply":{"id":"story","title":"📖 Story"}},
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

        set_quiz(sender,s["quiz"]["answer"])

        send_buttons(sender,s["quiz"]["question"],[
            {"type":"reply","reply":{"id":"a","title":s["quiz"]["options"]["a"]}},
            {"type":"reply","reply":{"id":"b","title":s["quiz"]["options"]["b"]}},
            {"type":"reply","reply":{"id":"c","title":s["quiz"]["options"]["c"]}}
        ])

        return "ok",200

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

app.run(host="0.0.0.0",port=10000)
