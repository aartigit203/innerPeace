from utils.json_utils import load_json, save_json
from datetime import date

FILE = "data/streak.json"

def update_streak(user):
    data = load_json(FILE)

    today = date.today()
    today_str = str(today)

    if user not in data:
        data[user] = {"count": 1, "last": today_str}
    else:
        last_date = date.fromisoformat(data[user]["last"])
        diff = (today - last_date).days

        if diff == 0:
            pass  # already counted today
        elif diff == 1:
            data[user]["count"] += 1
        else:
            data[user]["count"] = 1

        data[user]["last"] = today_str

    save_json(FILE, data)
    return data[user]["count"]
