import json
import pandas as pd


with open("festival_events.json") as f:
    data = json.load(f)

for item in data:
    print(f"Name = {item["name"]} and city = {item["location"]["city"]}") #2,3 Displaying the name and the city location

print("\n Printing events with more than 700 visitors") #4
for item in data:
    if item["visitors"] > 700:
        print(item["name"])


print("\n Printing features") #5
field_to_check = "features"
for item in data:
    if field_to_check not in item or["features"] is None:
        print(f" {item["event_id"]} having name {item["name"]} has no features listed")
    else:
        print(f" {item["event_id"]} having name {item["name"]} has {item["features"]} features listed")

df = pd.read_json("festival_events.json") #6
print(df)