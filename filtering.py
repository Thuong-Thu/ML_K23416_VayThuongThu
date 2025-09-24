from numpy import nan as NA
import pandas as pd

#Lọc dữ liệu bị thiếu
data = pd.DataFrame([[1., 6.5, 3.],
                     [1., NA, NA],
                     [NA, NA, NA],
                     [NA, 6.5, 3.]])
print(data)
print("-"*10)
cleaned = data.dropna() #bỏ dòng chứa NA
print(cleaned)
print("-" * 10)
cleaned2=data.dropna(how='all') #bỏ dòng toàn NA
print(cleaned2)
print("-" * 10)
cleaned3 = data[(data >= 0).all(axis=1)] #Bỏ dòng toàn âm
print(cleaned3)