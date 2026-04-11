from utils.json_utils import load_json, save_json
from datetime import datetime

FILE = "data/streak.json"

def update_streak(user):
    data = load_json(FILE)
    today = str(datetime.now().date())

    if user not in data:
        data[user] = {"count": 1, "last": today}
    else:
        last = data[user]["last"]
        diff = (datetime.now().date() - datetime.fromisoformat(last).date()).days

        if diff == 1:
            data[user]["count"] += 1
        elif diff > 1:
            data[user]["count"] = 1

        data[user]["last"] = today

    save_json(FILE, data)
    return data[user]["count"]
