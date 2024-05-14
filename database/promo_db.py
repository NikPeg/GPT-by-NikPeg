from . import cursor, database


def check_promo(promo):
    cursor.execute("SELECT sale FROM Promo WHERE name=?", (promo,))
    sale = cursor.fetchone()
    if sale is None:
        return 0
    return int(sale[0])


def add_promo(sale, count, name):
    cursor.execute(
        "INSERT INTO Promo(sale, count, name) VALUES(?,?,?,?)",
        (sale, count, name),
    )
    database.commit()