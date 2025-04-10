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
    question TEXT,
    answer TEXT,
    UNIQUE(question, answer)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS aktiv_chatlar (
    chat_id INTEGER PRIMARY KEY
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS istifadeci_mesajlari (
    user_id INTEGER,
    message TEXT,
    UNIQUE(user_id, message)
)
""")

conn.commit()

def elave_et(sual, cavab):
    with lock:
        cursor.execute("INSERT OR REPLACE INTO chatbot (question, answer) VALUES (?, ?)", (sual.lower(), cavab))
        conn.commit()

def cavab(sual):
    with lock:
        cursor.execute("SELECT answer FROM chatbot WHERE question = ?", (sual.lower(),))
        result = cursor.fetchall()
        return [row[0] for row in result] if result else None

def aktiv_chat(chat_id):
    with lock:
        cursor.execute("INSERT OR IGNORE INTO aktiv_chatlar (chat_id) VALUES (?)", (chat_id,))
        conn.commit()

def deaktiv_chat(chat_id):
    with lock:
        cursor.execute("DELETE FROM aktiv_chatlar WHERE chat_id = ?", (chat_id,))
        conn.commit()

def aktivdir(chat_id):
    with lock:
        cursor.execute("SELECT 1 FROM aktiv_chatlar WHERE chat_id = ?", (chat_id,))
        return cursor.fetchone() is not None

def user_elave(user_id, mesaj):
    with lock:
        cursor.execute("INSERT OR REPLACE INTO istifadeci_mesajlari (user_id, message) VALUES (?, ?)", (user_id, mesaj))
        conn.commit()