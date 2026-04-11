from utils.json_utils import load_json, save_json

FILE = "data/quiz.json"

def set_quiz(user, answer):
    data = load_json(FILE)
    data[user] = {"answer": answer}
    save_json(FILE, data)

def get_quiz(user):
    return load_json(FILE).get(user, {}).get("answer")

def clear_quiz(user):
    data = load_json(FILE)
    if user in data:
        del data[user]
    save_json(FILE, data)
