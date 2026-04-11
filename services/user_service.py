from utils.json_utils import load_json, save_json

FILE = "data/users.json"

def add_user(user):
    users = load_json(FILE)
    if not isinstance(users, list):
        users = []
    if user not in users:
        users.append(user)
        save_json(FILE, users)
