import sqlite3
import os
from threading import Lock

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "..", "chatbot.db")
lock = Lock()
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chatbot (
    question TEXT PRIMARY KEY,
    answer TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS active_chats (
    chat_id INTEGER PRIMARY KEY
)
""")

conn.commit()
def add_pair(question, answer):
    with lock:
        cursor.execute("INSERT OR REPLACE INTO chatbot (question, answer) VALUES (?, ?)", (question.lower(), answer))
        conn.commit()

def get_answer(question):
    with lock:
        cursor.execute("SELECT answer FROM chatbot WHERE question = ?", (question.lower(),))
        result = cursor.fetchone()
        return result[0] if result else None
def activate_chat(chat_id):
    with lock:
        cursor.execute("INSERT OR IGNORE INTO active_chats (chat_id) VALUES (?)", (chat_id,))
        conn.commit()

def deactivate_chat(chat_id):
    with lock:
        cursor.execute("DELETE FROM active_chats WHERE chat_id = ?", (chat_id,))
        conn.commit()

def is_chat_active(chat_id):
    with lock:
        cursor.execute("SELECT 1 FROM active_chats WHERE chat_id = ?", (chat_id,))
        return cursor.fetchone() is not None