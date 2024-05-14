from . import cursor


def check_promo(user_id):
    cursor.execute("SELECT sale FROM Promo WHERE id=?", (user_id,))
    sale = cursor.fetchone()
    if sale is None:
        return 0
    return int(sale[0])