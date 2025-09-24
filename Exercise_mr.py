import pandas as pd

def find_orders_within_range(df, minValue, maxValue, SortType=True):
    # Tính tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(
        lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum(),
        include_groups=False
    ).reset_index(name='Sum')

    # Lọc trong khoảng [minValue, maxValue]
    orders_within_range = order_totals[
        (order_totals['Sum'] >= minValue) & (order_totals['Sum'] <= maxValue)
    ]

    # Sắp xếp theo SortType
    orders_sorted = orders_within_range.sort_values(
        by='Sum', ascending=SortType
    ).reset_index(drop=True)

    return orders_sorted


# --- Demo ---
df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

minValue = float(input('Nhập giá trị min: '))
maxValue = float(input('Nhập giá trị max: '))
SortType = input("SortType (True/False): ").strip().lower() == "true"

result = find_orders_within_range(df, minValue, maxValue, SortType)
print(result)
