import pandas as pd

def find_orders_within_range(df,minValue, maxValue):
    #tong gia tri tung don hang
    order_totals=df.groupby('OrderID').apply(lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())
    #loc don hang trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
    #danh sach cac ma don hang khong trung nhau
    unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()

    return unique_orders

df = pd.read_csv("../datasets/SalesTransactions/SalesTransactions.csv")

minValue = float(input('Nhap gia tri min: '))
maxValue = float(input('Nhap gia tri max: '))
result = find_orders_within_range(df,minValue,maxValue)
print('Danh sach cac hoa don trong pham vi gia tri tu',minValue, 'den', maxValue, 'la:',result)