import json
from collections import Counter
import pandas as pd

with open("smart_home_devices.json") as f:
    data = json.load(f)

# print(data)
# 2
# for i,elem in enumerate(data):
#     print(elem['device_id'], elem['device_type'],elem['room'])

# # 3
# for elem in data:
#     if elem['status'] == "Active":
#         print(elem)

# 4
# for elem in data:
#     if elem['metrics']['battery']  < 60:
#         print(elem)

# 5
# field_to_check = "temperature"
# for elem in data:
#     if field_to_check in elem['metrics']:
#         print(elem)

# 6
# field_to_check = 'alerts'
# for elem in data:
#     if field_to_check in elem:
#         print(elem)

# 7
# device_counts = Counter(elem['device_type'] for elem in data if 'device_type' in elem )
# for device_type,count in device_counts.items():
#     print(device_type,count)

# 8
for elem in data:
    if elem["metrics"]["battery"] >= 70:
        elem["health"] = 'Good'
    elif elem["metrics"]["battery"] >50 and elem["metrics"]["battery"] < 69:
        elem["health"] = 'Moderate'
    elif elem["metrics"]["battery"] < 50:
        elem["health"] = 'Low'
# 9
with open("device_health_report.json",'w') as f:
    json.dump(data,f,indent=4)

df = pd.json_normalize(data)

# print(df[["device_id","device_type","room","status","metrics.battery","health"]])

# Extra
print(df[(df["status"] == "Active") | (df["metrics.battery"] < 70)])