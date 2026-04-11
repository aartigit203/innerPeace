from utils.json_utils import load_json, save_json
from datetime import datetime

FILE = "data/streak.json"

def update_streak(user):
    data = load_json("streak.json")

    today = datetime.date.today()
    today_str = str(today)

    if user not in data:
        data[user] = {"count": 1, "last": today_str}
    else:
        last_date = datetime.date.fromisoformat(data[user]["last"])
        diff = (today - last_date).days

        if diff == 0:
            pass  # already counted today

        elif diff == 1:
            data[user]["count"] += 1  # continue streak

        else:
            data[user]["count"] = 1  # reset streak gently

        data[user]["last"] = today_str

    save_json("streak.json", data)
    
    return data[user]["count"]
