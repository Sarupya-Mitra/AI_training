import json
import pandas as pd

with open("support_ticket.json") as json_file:
    data = json.load(json_file)

df = pd.json_normalize(data)

print(df)