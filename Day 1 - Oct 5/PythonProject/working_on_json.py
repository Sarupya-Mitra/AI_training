import json
import pandas as pd

with open("support_ticket.json") as json_file:
    data = json.load(json_file)


for ticket in data:
    print(f"{ticket["customer"]["name"]}")

print(data[1].get("priority","Not Assigned"))
