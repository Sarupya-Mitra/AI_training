import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}

df = pd.DataFrame(data)

df["Total"] = df["Quantity"] * df["Price"]

sales = df.groupby("Product")["Total"].sum()

sales.plot(kind = "bar")
plt.title("Sales by Product")
plt.xlabel("Product",rotation = 0)
plt.xticks(rotation = 0)
plt.ylabel("Total Sales")
plt.show()