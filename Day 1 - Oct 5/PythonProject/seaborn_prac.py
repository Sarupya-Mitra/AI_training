import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}

df = pd.DataFrame(data)

df["Total"] = df["Quantity"] * df["Price"]

sns.barplot(data=df, x="Product", y="Total")

plt.title("Sales by Product")
plt.show()
