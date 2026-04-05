from flask import Flask, request
import requests, os, json, threading, time
from datetime import datetime

from stories import get_story
from shlokas import get_shloka_response
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# ================= JSON HELPERS =================
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


def update_conversation(user, message):
    conv = load_json("conversation.json")
    if user not in conv:
        conv[user] = []
    conv[user].append(message)

    # keep only last 5 messages
    conv[user] = conv[user][-5:]
    save_json("conversation.json", conv)

def update_profile(user, text):
    profiles = load_json("profiles.json")

    if user not in profiles:
        profiles[user] = {
            "name": "",
            "topics": {}
        }

    # Detect name (simple pattern)
    if "my name is" in text:
        name = text.split("my name is")[-1].strip().title()
        profiles[user]["name"] = name

    # Track topics
    keywords = ["stress", "career", "anxiety", "sad", "fear"]

    for k in keywords:
        if k in text:
            profiles[user]["topics"][k] = profiles[user]["topics"].get(k, 0) + 1

    save_json("profiles.json", profiles)


def get_conversation(user):
    conv = load_json("conversation.json")
    return " ".join(conv.get(user, []))
# ================= LOAD STATE =================
user_mode = load_json("user_memory.json")
user_quiz = load_json("quiz.json")
user_streak = load_json("streak.json")
leaderboard = load_json("leaderboard.json")
processed = set()

# ================= SAVE USER =================
def save_user(num):
    users = load_json("users.json")
    if not isinstance(users, list):
        users=[]
    if num not in users:
        users.append(num)
        save_json("users.json", users)

# ================= SEND =================
def send_message(to, msg):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":msg}}
    )

def send_buttons(to, body, buttons):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={
            "messaging_product":"whatsapp",
            "to":to,
            "type":"interactive",
            "interactive":{"type":"button","body":{"text":body},"action":{"buttons":buttons}}
        }
    )

def send_image(to, url, caption=""):
    requests.post(
        f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"messaging_product":"whatsapp","to":to,"type":"image","image":{"link":url,"caption":caption}}
    )

# ================= AI =================
def ai_reply(text):
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"Krishna guiding peacefully"},
                      {"role":"user","content":text}],
            timeout =5 #prevents hanging 
        )
        return "🌸 Hare Krishna 🙏\n\n" + r.choices[0].message.content
    except EXCEPTION as e:
        print("AI failed:", e)
        # fallback ALWAYS works
        return get_shloka_response(text)

# ================= DAILY =================
def broadcast():
    while True:
        now = datetime.now()
        if now.hour == 7 and now.minute == 0:
            users = load_json("users.json")
            s = get_story()
            for u in users:
                send_message(u, f"🌅 Good Morning 🌸\n\n{s['text'][:250]}")
            time.sleep(60)
        time.sleep(20)

threading.Thread(target=broadcast, daemon=True).start()

# ================= PROFILE =================
def get_profile_context(user):
    profiles = load_json("profiles.json")

    profile = profiles.get(user, {})
    name = profile.get("name", "")
    topics = profile.get("topics", {})

    top_topic = ""

    if topics:
        top_topic = max(topics, key=topics.get)

    return name, top_topic

# ================= WEBHOOK =================
@app.route("/webhook", methods=["GET","POST"])
def webhook():

    if request.method=="GET":
        if request.args.get("hub.verify_token")==VERIFY_TOKEN:
            return request.args.get("hub.challenge"),200
        return "error",403

    data=request.json

    try:
        msg=data["entry"][0]["changes"][0]["value"]["messages"][0]

        mid=msg["id"]
        if mid in processed: return "ok",200
        processed.add(mid)

        sender=msg["from"]
        save_user(sender)

        text = msg["interactive"]["button_reply"]["id"] if "interactive" in msg else msg["text"]["body"].lower()
        update_profile(sender,text)
        update_conversation(sender, text)
        

        # 🌸 MENU
        if text in ["hi","menu"]:
            user_mode[sender]=None
            save_json("user_memory.json",user_mode)

            send_buttons(sender,
                "🌸 Hare Krishna 🙏\n\nChoose your path ✨",
                [
                    {"type":"reply","reply":{"id":"inner","title":"🧘 Peace"}},
                    {"type":"reply","reply":{"id":"bal","title":"👶 Stories"}}
                ])
            return "ok",200

        # SELECT
        if text in ["inner"]:
            user_mode[sender]="inner"
            save_json("user_memory.json",user_mode)
            send_message(sender,"🧘 Tell me what you feel 💭")
            return "ok",200

        if text in ["bal"]:
            user_mode[sender]="bal"
            save_json("user_memory.json",user_mode)

            send_buttons(sender,"👶 Balgokulam 🌸",
                [
                    {"type":"reply","reply":{"id":"story","title":"📖 Story"}},
                    {"type":"reply","reply":{"id":"leader","title":"🏆 Leaderboard"}}
                ])
            return "ok",200

        # QUIZ ANSWER
        if sender in user_quiz and text.startswith("opt_"):

            correct=user_quiz[sender]["answer"]

            # STREAK
            today=str(datetime.now().date())
            prev=user_streak.get(sender,{"count":0,"last":""})

            if prev["last"]!=today:
                prev["count"]+=1
                prev["last"]=today

            user_streak[sender]=prev
            save_json("streak.json",user_streak)

            # LEADERBOARD
            leaderboard[sender]=prev["count"]
            save_json("leaderboard.json",leaderboard)

            if text==correct:
                msg="✨ Correct! Krishna is happy 💛"
            else:
                msg=f"💛 Correct answer: {correct}"

            send_buttons(sender,
                f"{msg}\n🔥 Streak: {prev['count']}",
                [
                    {"type":"reply","reply":{"id":"next","title":"➡️ Next"}},
                    {"type":"reply","reply":{"id":"leader","title":"🏆 Leaderboard"}}
                ])

            del user_quiz[sender]
            save_json("quiz.json",user_quiz)
            return "ok",200

        # STORY FLOW
        if user_mode.get(sender)=="bal":

            if text in ["story","next"]:
                s=get_story()

                #send_image(sender,s["image"],s["title"])
                send_message(sender,s["text"])

                send_buttons(sender,s["quiz_question"],
                    [{"type":"reply","reply":opt} for opt in s["quiz_options"]])

                user_quiz[sender]={"answer":s["answer"]}
                save_json("quiz.json",user_quiz)

            elif text=="leader":
                top=sorted(leaderboard.items(),key=lambda x:x[1],reverse=True)[:5]
                msg="🏆 Top Learners\n\n"
                for i,(u,c) in enumerate(top,1):
                    msg+=f"{i}. {u[-4:]} → {c}🔥\n"

                send_message(sender,msg)

            return "ok",200

        # INNER PEACE
        if user_mode.get(sender)=="inner":
            print("User asked:", text)
            context = get_conversation(sender) + "" + text
            base_response = get_shloka_response(context)

            name, topic = get_profile_context(sender)

            # Personalize greeting
            if name:
                greeting = f"🌸 Hare Krishna {name} 🙏\n\n"
            else:
                greeting = "🌸 Hare Krishna 🙏\n\n"

            # Add pattern awareness
            if topic:
                insight = f"I notice you’ve been thinking about {topic} lately 🌿\n\n"
            else:
                insight = ""

            final_response = greeting + insight + base_response.replace("🌸 Hare Krishna 🙏\n\n", "")
        
            if "Krishna is with you" not in final_response:
                send_message(sender,final_response)
            else:
                send_message(sender,ai_reply(text))
            return "ok",200

    except Exception as e:
        print(e)

    return "ok",200

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
