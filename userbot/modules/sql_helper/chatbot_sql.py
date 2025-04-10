import threading
from sqlalchemy import Column, String
from userbot.modules.sql_helper import BASE, SESSION
class ChatBot(BASE):
    __tablename__ = "chatbot"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)
ChatBot.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()
def ids(chat_id):
    try:
        chat = SESSION.query(ChatBot).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()
def userbot(chat_id):
    with INSERTION_LOCK:
        tchat = SESSION.query(ChatBot).get(str(chat_id))
        if not tedechat:
            tchat = ChatBot(str(chat_id))
        SESSION.add(tchat)
        SESSION.commit()


def chatbot(chat_id):
    with INSERTION_LOCK:
        tchat = SESSION.query(ChatBot).get(str(chat_id))
        if tedechat:
            SESSION.delete(tchat)
        SESSION.commit()