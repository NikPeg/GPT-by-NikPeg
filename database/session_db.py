from loader import gpt
from . import database, cursor


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
    cursor.execute("SELECT run FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    run_id = cursor.fetchone()
    if not (run_id and run_id[0]):
        return None
    return run_id[0]


def set_run_id(user_id, run_id):
    print("!!!!!!!!!set run")
    print(user_id, run_id)
#     cursor.execute(
#         """UPDATE Session
# SET run = ?
# WHERE id = (
#     SELECT id
# FROM Session
# WHERE user_id = ?
# ORDER BY id DESC
# LIMIT 1
# );""",
#         (run_id, user_id),
#     )
#     database.commit()
