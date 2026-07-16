# database.py
from datetime import datetime
import json
import os

DB_FILE = "lessons.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading database: {e}")
        return {}

def save_lesson(user_id: int, lesson_name: str, words: list):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str not in db:
        db[user_id_str] = {}
        
    words_data = {}
    for w in words:
        words_data[w] = {
            "translation": None,
            "audio": None,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "next_review": None
        }


    db[user_id_str][lesson_name] = {
        "words": words_data,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing to database: {e}")
    
    def lesson_exists(user_id: int, lesson_name: str) -> bool:
        db = load_db()
        user_id_str = str(user_id)
        return user_id_str in db and lesson_name in db[user_id_str]