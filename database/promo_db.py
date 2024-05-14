from . import cursor, database


def check_promo(promo):
    cursor.execute("SELECT count, sale FROM Promo WHERE name=?", (promo,))
    res = cursor.fetchone()
    if res is None or res[0] <= 0:
        return 0
    cursor.execute("UPDATE Promo SET count = count - 1 WHERE name = ?;", (promo,))
    database.commit()
    return int(res[0][1])


def add_promo(sale, count, name):
    cursor.execute(
        "INSERT INTO Promo(sale, count, name) VALUES(?,?,?,?)",
        (sale, count, name),
    )
    database.commit()