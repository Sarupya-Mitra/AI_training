with open("airport_operations.txt") as f:
    data = f.read()

# print(data)

words = data.split()

with open("airport_operations.txt") as f:
    lines = f.readlines()
# Read total characters
with open("airport_operations.txt") as f:
    chars = list(f.read())

# print(f"Total no of characters : {len(chars)}")
# print(f"Total no of words : {len(words)}")
# print(f"Total no of lines : {len(lines)}")

# 3
# print(f" Count of flight , 'runway' , 'operations' , 'reported' are \n"
#       f"{data.lower().count("flight") , data.lower().count("runway") , data.lower().count("operations") , data.lower().count("reported")}")

# 4
# print("Printing lines with word 'runway'")
# for line in lines:
#     if 'runway' in line:
#         print(line)

# 5
# print("Printing lines with either delay or delayed or delays")
# for line in lines:
#     if ('delay' or 'delayed' or 'delays') in line:
#         print(line)

# 6 Extract lines which mention anything reported
# for line in lines:
#     if'report' in line:
#         print(line)

# 7 Words to search
# words_to_search = {'emergency':False ,
#                    'inspection' : False,
#                    'weather' : False,
#                    'passengers': False,
#                    'maintenance' : False
#                    }
#
# for word in words_to_search:
#     if word in words:
#         words_to_search[word] = True
# for k,v in words_to_search.items():
#     print(k,v)

# 8
# count_words_dict = {"flight" : 0,
#                     "runway" : 0,
#                     "operations" : 0,}
#
# for word in count_words_dict:
#     if word in words:
#         count_words_dict[word] += 1
#
# for k,v in count_words_dict.items():
#     print(k,v)

# 9 Printing the longest line
# print(max(lines))

# 10
# new_lines = []
for line in lines:
    if ('delay' or 'weather') in line:
        # new_lines.append(line)
        with open("filtered_airport_report.txt",'a') as f:
           f.write(line)



