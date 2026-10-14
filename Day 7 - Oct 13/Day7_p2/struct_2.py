import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("renewable_energy.csv")  #1
# print(df.head(1))

#2. printing only solar or wind type energy type
# print(df[(df["Energy_Type"] == "Solar") | (df["Energy_Type"] == "Wind")])

# 3. Adding New Column
df["Efficiency_Percent"] = (df["Actual_Output_MW"] / df["Capacity_MW"]) * 100
# print(df)

# 4.
#print(f" Plants with more than 85% efficiency: {df[(df["Efficiency_Percent"] > 85)]}")

# 5
# print(f"Avg energy for each energy type: \n "
#       f"{df.groupby("Energy_Type")['Efficiency_Percent'].mean()}")

# 6
# print(f"Displaying maintenance cost for each energy type: \n"
#       f"{df.groupby("Energy_Type")["Maintenance_Cost"].sum()}")

# 7 Displaying data where output power is maximum
# print(df[df["Actual_Output_MW"] == df["Actual_Output_MW"].max()])

# 8
df["Cost_per_MW"] = df["Maintenance_Cost"] / df["Actual_Output_MW"]
# print(df)

# 9
# print(df.sort_values("Cost_per_MW",ascending=True))

# 10
print(df[(df['Efficiency_Percent'] > 80) & (df['Maintenance_Cost'] < 70000)])
# Extra
sns.barplot(x="Plant_Name", y="Efficiency_Percent", data=df)
plt.show()