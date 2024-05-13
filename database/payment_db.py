from . import cursor, database
import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
GIFT_DAY = datetime.datetime(2024, 4, 27)


def check_subscribed(user_id):
    cursor.execute("SELECT register FROM User WHERE id=?", (user_id,))
    register = datetime.datetime.strptime(cursor.fetchone()[0], DATE_FORMAT)
    if register + datetime.timedelta(days=2) >= datetime.datetime.now():
        return True
    if register <= GIFT_DAY and datetime.datetime.now() <= GIFT_DAY + datetime.timedelta(days=30):
        return True
    cursor.execute("SELECT subscribed FROM User WHERE id=?", (user_id,))
    subscribed = bool(cursor.fetchone()[0])
    return subscribed


def subscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 1 WHERE id=?;", (user_id,))
    database.commit()


def unsubscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 0 WHERE id=?;", (user_id,))
    database.commit()
