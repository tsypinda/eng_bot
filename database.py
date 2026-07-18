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

def delete_lesson(user_id: int, lesson_name: str):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str in db and lesson_name in db[user_id_str]:
        del db[user_id_str][lesson_name]
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error writing to database: {e}")

def add_words(user_id: int, lesson_name: str, new_words: list):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str not in db or lesson_name not in db[user_id_str]:
        print(f"Lesson '{lesson_name}' for user {user_id} does not exist.")
        return
    
    words_data = db[user_id_str][lesson_name]["words"]
    
    for w in new_words:
        if w not in words_data:
            words_data[w] = {
                "translation": None,
                "audio": None,
                "correct_answers": 0,
                "incorrect_answers": 0,
                "next_review": None
            }
    
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing to database: {e}")

def remove_words(user_id: int, lesson_name: str, words_to_remove: list):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str not in db or lesson_name not in db[user_id_str]:
        print(f"Lesson '{lesson_name}' for user {user_id} does not exist.")
        return
    
    words_data = db[user_id_str][lesson_name]["words"]
    
    for w in words_to_remove:
        if w in words_data:
            del words_data[w]
    
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing to database: {e}")

def show_lessons(user_id: int):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str not in db:
        return []
    
    return list(db[user_id_str].keys())

def show_words(user_id: int, lesson_name: str):
    db = load_db()
    user_id_str = str(user_id)
    
    if user_id_str not in db or lesson_name not in db[user_id_str]:
        return []
    
    return list(db[user_id_str][lesson_name]["words"].keys())


    