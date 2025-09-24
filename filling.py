from numpy import nan as NA
import pandas as pd

# Điền dữ liệu còn thiếu
data = pd.DataFrame([[1., 6.5, 3.],
                  	[2., NA, NA],
                  	[NA, NA, NA],
                  	[3, 6.5, 3.],
                    [4, 6.5, 3.],
                    [5, 6.5, 3.],
                    [NA, NA, NA],
                    [6, 6.5, 3.]])
print(data)
print("-"*10)
cleaned=data.fillna(data.mean())
print(cleaned)