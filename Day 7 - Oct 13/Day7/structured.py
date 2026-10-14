import pandas as pd
import seaborn as sns
df = pd.read_csv("structured_data.csv")

# print(df)  # 1

# print(df[["Shipment_ID","Origin","Destination","Cost"]]) # 2

# print(df[df["Mode"] == 'Road']) # 3.Showing shipments whose mode is Road

# print(df[df["Weight_Kg"] > 150]) # 4

# 5. Creating a new column
# df['Cost_per_Km'] = df['Cost'] / df['Distance_Km']
# df.to_csv("structured_data.csv")

# 6
# print(f"Mean Shipment cost is : {df["Cost"].mean()}")
# print(f"Max Shipment cost is : {df["Cost"].max()}")
# print(f"Min Shipment Cost is {df["Cost"].min()}")

# 7,8
# print(f"Grouping by Mode, the total cost is {df.groupby('Mode')['Cost'].sum()} "
#       f"and the avg cost is {df.groupby('Mode')['Cost'].mean()}")

# 9
# print(f"Sorting Shipments from highest to lowest cost : \n {df.sort_values('Cost',ascending=False)}")

# 10
print(f"Shipments with delivery days <= 1 and Cost < 5000 \n"
      f"{df[(df['Delivery_Days'] <= 1) & (df['Cost'] < 5000) ]}")



