from . import cursor


def check_promo(promo):
    cursor.execute("SELECT sale FROM Promo WHERE name=?", (promo,))
    sale = cursor.fetchone()
    if sale is None:
        return 0
    return int(sale[0])