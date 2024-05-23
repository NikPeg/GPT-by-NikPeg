from . import database, cursor
from loader import gpt


def create_new_session(user_id):
    thread_id = gpt.create_thread()
    cursor.execute("INSERT INTO Session(user_id, thread_id) VALUES(?, ?)", (user_id, thread_id,))
    database.commit()
    cursor.execute("SELECT id FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    return int(cursor.fetchone()[0])


def get_user_session_id(user_id):
    cursor.execute("SELECT id FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    session_id = cursor.fetchone()
    if session_id is None:
        return create_new_session(user_id)
    return int(session_id[0])


def get_thread_id(user_id):
    cursor.execute("SELECT thread_id FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    thread_id = cursor.fetchone()
    if not (thread_id and thread_id[0]):
        create_new_session(user_id)
        return get_thread_id(user_id)
    return thread_id[0]


def get_run_id(user_id):
    cursor.execute("SELECT run_id FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    run_id = cursor.fetchone()
    if not (run_id and run_id[0]):
        create_new_session(user_id)
        return get_run_id(user_id)
    return run_id[0]
