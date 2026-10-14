import json
import pandas as pd

with open ("semi_structured.json") as file:
    data = json.load(file)

# print(data) #1

# 2 printing the incident IDs
# for incidents in data:
#     print(incidents["incident_id"])

# 3 printing the city
# for inc in data:
#     print(inc["location"]["city"])

# 4 High severe incidents
# for inc in data:
#     if inc["severity"] == "High":
#         print(inc["incident_id"])

# 5 Safety category incidents
# for inc in data:
#     if inc["category"] == "Safety":
#         print(inc["incident_id"])

# 6
# field = "actions"
# for inc in data:
#     if field not in inc:
#         print(f"{inc['incident_id'] } has no actions recorded")
#     else:
#         print(f"{inc['incident_id']} has {inc['actions']} actions")

# 7
# count_high = 0
# count_medium = 0
# count_low = 0
# for inc in data:
#     if inc['severity'] == "High":
#         count_high += 1
#     elif inc['severity'] == "Medium":
#         count_medium += 1
#     elif inc['severity'] == "Low":
#         count_low += 1
# print(f"The count of the incidents: \n"
#       f"High = {count_high}, Medium = {count_medium}, Low = {count_low}")

#
# 8,9
# for inc in data:
#     inc['status'] = 'Open'
#
# with open('updated_incidents.json','w') as file2:
#     json.dump(data,file2,indent=4)

# 10
df = pd.json_normalize(data)
# print(df.head())
print(df[["incident_id","severity","category","location.city","location.site"]])