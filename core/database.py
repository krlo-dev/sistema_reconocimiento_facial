import csv
import os
import pickle
from datetime import datetime

FACES_DIR = os.path.join("data", "faces")
LOG_FILE = os.path.join("data", "access_log.csv")
DB_FILE = os.path.join("data", "users.db")

os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

def save_access(name, user_id):
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, user_id])

def load_access_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, mode="r") as file:
        reader = csv.reader(file)
        return [{"timestamp": row[0], "name": row[1], "user_id": row[2]} for row in reader]

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "rb") as f:
        return pickle.load(f)

def save_users(users):
    with open(DB_FILE, "wb") as f:
        pickle.dump(users, f)

def add_user_to_db(name, user_id, encoding):
    users = load_users()
    users[user_id] = {'name': name, 'encoding': encoding}
    save_users(users)

def remove_user_from_db(name, user_id):
    users = load_users()
    if user_id in users:
        del users[user_id]
        save_users(users)

def get_all_users():
    users = load_users()
    return [{'user_id': uid, 'name': data['name'], 'encoding': data['encoding']} for uid, data in users.items()]
