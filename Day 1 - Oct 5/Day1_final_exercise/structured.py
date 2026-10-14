import pandas as pd

df = pd.read_csv("library_loans.csv")  # 1. Loading to DF
print(df)
# 2. Displaying only Member, Book Category, Fine
print(df[["Member_Name","Book_Category","Fine"]])

# 3. Show members whose fine is >50
print(df[df["Fine"] > 50])

# 4. Creating new col named Status
df["Status"] = df["Fine"] > 0
# print(df["Status"])
df["Status"] = ["Fine Due" if x == True else "No Fine" for x in df["Status"]]
print(df["Status"])
#5 Avg no of days borrowed
print("Avg days borrowed" + df["Days_Borrowed"].mean())
#6 Total fine collected by different Book Categories
print(df.groupby("Book_Category")["Fine"].sum())