import datetime

from . import *


def add_in_feedback_users(user_id):
    check_ = check_user_in_feedback(user_id)
    if not check_:
        cursor.execute("INSERT INTO UserFeedback VALUES(?)", (user_id,))
        database.commit()


def check_user_in_feedback(user_id):
    cursor.execute("SELECT user_id FROM UserFeedback WHERE user_id=?", (user_id,))
    user_check = cursor.fetchone()
    if user_check is None:
        return False
    return True


def delete_user_from_feedback(user_id):
    cursor.execute("DELETE FROM UserFeedback WHERE user_id=?", (user_id,))
    database.commit()


def get_all_feed_back_users():
    cursor.execute(
        """SELECT uf.user_id 
FROM UserFeedback uf 
JOIN User u ON uf.user_id = u.id 
WHERE u.register <= datetime('now', '-1 minute')
"""
    )
    all_users = cursor.fetchall()
    return all_users


def get_all_subscriptions():
    cursor.execute("SELECT id, name, subscribed FROM User")
    all_users = cursor.fetchall()
    return all_users


def add_new_feedback(user_id, user_text):
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO Feedback VALUES(?,?,?)", (user_id, user_text, date,))
    database.commit()
