import datetime

from gpt.models import MessageDTO, Role
from . import database, cursor
from .session_db import get_user_session_id


def add_new_message(user_id, user_request, bot_answer):
    session_id = get_user_session_id(user_id)
    cursor.execute(
        "INSERT INTO Message(user_id, user_request, bot_answer, session_id) VALUES(?,?,?,?)",
        (user_id, user_request, bot_answer, session_id,),
    )
    database.commit()


def get_conversation_by_user(user_id):
    session_id = get_user_session_id(user_id)
    cursor.execute("SELECT * FROM Message WHERE session_id=?", (session_id,))
    res = cursor.fetchall()
    conversation = []
    for message in res:
        conversation.append(MessageDTO(Role.USER, message[1]))
        conversation.append(MessageDTO(Role.ASSISTANT, message[2]))
    return conversation
