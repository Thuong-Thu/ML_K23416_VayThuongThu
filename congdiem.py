import pandas as pd

df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

def top3_best_selling_products(df):
    # Tính giá trị bán ra cho từng sản phẩm
    df['SalesValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Tính tổng giá trị bán ra theo ProductID
    product_totals = (
        df.groupby('ProductID')['SalesValue']
        .sum()
        .reset_index()
    )

    # Sắp xếp giảm dần theo SalesValue và lấy top 3
    top3 = product_totals.sort_values(
        by='SalesValue', ascending=False
    ).head(3).reset_index(drop=True)

    return top3

result = top3_best_selling_products(df)
print(result)
