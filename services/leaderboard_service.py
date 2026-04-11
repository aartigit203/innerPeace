from utils.json_utils import load_json, save_json

FILE = "data/leaderboard.json"

def update_score(user):
    scores = load_json(FILE)
    scores[user] = scores.get(user, 0) + 1
    save_json(FILE, scores)

def get_leaderboard():
    scores = load_json(FILE)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
