from . import cursor, database
import datetime

from .user_db import get_sale

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def check_subscribed(user_id):
    cursor.execute("SELECT register FROM User WHERE id=?", (user_id,))
    result = cursor.fetchone()
    if not result:
        return False
    register = datetime.datetime.strptime(result[0], DATE_FORMAT)
    if register + datetime.timedelta(days=2) >= datetime.datetime.now():
        return True
    cursor.execute("SELECT subscribed FROM User WHERE id=?", (user_id,))
    subscribed = bool(cursor.fetchone()[0])
    if not subscribed:
        sale = get_sale(user_id)
        return sale == 100
    return subscribed


def subscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 1 WHERE id=?;", (user_id,))
    database.commit()


def unsubscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 0 WHERE id=?;", (user_id,))
    database.commit()
