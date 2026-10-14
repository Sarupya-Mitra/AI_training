import pandas as pd

data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}

df = pd.DataFrame(data)

print(df)

# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.dtypes)

print("######")

df["Total"] = df["Quantity"] * df["Price"]
# print(df.groupby("Product")["Total"].sum())
print(df.sort_values(by="Total", ascending=True))
