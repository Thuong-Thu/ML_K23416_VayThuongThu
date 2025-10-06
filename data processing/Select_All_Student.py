import sqlite3

def top_n_customers_sqlite(db_path, n):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    sql = """
        SELECT i.CustomerId, SUM(i.Total) AS TotalSpent
        FROM Invoice AS i
        GROUP BY i.CustomerId
        ORDER BY TotalSpent DESC
        LIMIT ?;
    """
    cur.execute(sql, (n,))
    rows = cur.fetchall()
    cur.close(); con.close()
    return rows

# dùng:
# rows = top_n_customers_sqlite("Chinook_Sqlite.sqlite", 5)
# print(rows)
