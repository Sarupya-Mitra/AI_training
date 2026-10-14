import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "Employee": ["Aisha", "Rahul", "Neha", "Omar", "Priya", "Karan", "Fatima", "Vikram"],
    "Department": ["HR", "IT", "Finance", "IT", "HR", "Finance", "IT", "HR"],
    "Training_Hours": [12, 18, 10, 22, 15, 8, 20, 14],
    "Assessment_Score": [78, 88, 72, 91, 84, 69, 95, 80],
    "Completed": ["Yes", "Yes", "No", "Yes", "Yes", "No", "Yes", "Yes"]
}
df = pd.DataFrame(data)
#print(df)  # Whole df display
print("######")
#print(df.head(4))  # Top 4 rows
print("######")
#print(df[["Employee","Assessment_Score"]])  # 2 cols
print("######")
#print(df[df["Department"]== "IT"])  # IT info
print("######")
#print(df[df["Assessment_Score"]>80])  # Greater than 80 score
print("######")
#print(df[df["Completed"] == "Yes"])  #Completed data
print("######")
#print(df[(df["Department"] == "IT") & (df["Assessment_Score"] > 85)])  # two constraints
print("######")
# Creating a new column "passed"
df["Passed"] = df["Assessment_Score"] >= 75
df["Passed"] = ["Pass" if x == True else "Fail" for x in df["Passed"]]
print(df["Passed"])
print("######")
print(np.mean(df["Assessment_Score"]))  # Avg score
print("######")
# Max and Min scores:
print(f"Max Score: {np.max(df["Assessment_Score"])} and Min Score: {np.min(df["Assessment_Score"])}")
print("######")
print(np.mean(df["Training_Hours"]))  # Avg Training hrs
print("######")

print(df.sort_values("Assessment_Score", ascending=False)) # Assessment score sort
print("######")

print(df.groupby("Department")["Assessment_Score"].mean()) #Mean of score grouped by dept
print("######")

print(df.groupby("Department")["Training_Hours"].sum())  # Total train hrs of each dept
print("######")

print(df.groupby("Department")["Employee"].count())  # Count of employees in each dept
print("######")

print(f"Employees who completed training : {(df["Completed"] == True).count()}")

scores = df["Assessment_Score"].to_numpy()
print(f"Type of scores: {type(scores)}")
print(f"Scores \n Mean = {np.mean(scores)} \n Max = {np.max(scores)}"
      f"\n Min = {np.min(scores)} \n Std = {np.std(scores)}")

dept_wise_avg_Score = df.groupby("Department")["Assessment_Score"].mean()
dept_wise_avg_Score.plot(kind="bar")
plt.xlabel("Department")
plt.xticks(rotation = 0)
plt.ylabel("Avg Score")
plt.title("Avg score per Dept")
plt.show()


dept_wise_train_hrs = df.groupby("Department")["Training_Hours"].sum()
dept_wise_train_hrs.plot(kind="bar")
plt.xlabel("Department")
plt.xticks(rotation = 0)
plt.ylabel(" Total Train hrs")
plt.title("Total Train hrs per Dept")
plt.show()

sns.barplot(x="Department", y="Assessment_Score", data=df)
plt.title("Scores by Dept")
plt.show()
