import pandas as pd
df = pd.read_csv("file.csv")
print(df)

print(df.columns ,"\n", df.shape , "\n" , df.dtypes)

print(df[["Station","kWh", "Amount"]])

print(df[df["Station"] == "ChargePoint-C"])