import sqlite3
import pandas as pd

def top_n_customers(db_path, n):
    try:
        # Kết nối DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("DB Init")

        # Query: chỉ lấy CustomerId, FirstName và TotalSpent
        query = """
            SELECT c.CustomerId,1
                   c.FirstName,
                   SUM(il.UnitPrice * il.Quantity) AS TotalSpent
            FROM InvoiceLine il
            JOIN Invoice inv ON inv.InvoiceId = il.InvoiceId
            JOIN Customer c ON c.CustomerId = inv.CustomerId
            GROUP BY c.CustomerId, c.FirstName
            ORDER BY TotalSpent DESC
            LIMIT ?;
        """
        cursor.execute(query, (n,))

        # Lấy dữ liệu vào DataFrame
        df = pd.DataFrame(
            cursor.fetchall(),
            columns=["CustomerId", "FirstName", "TotalSpent"]
        )
        return df

    except sqlite3.Error as error:
        print("Error occurred:", error)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("sqlite connection closed")


# ---------------------------
# Test hàm
result = top_n_customers("../databases/Chinook_Sqlite.sqlite", n=6)
print(result)
