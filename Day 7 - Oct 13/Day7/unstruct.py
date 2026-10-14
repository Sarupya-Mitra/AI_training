with open("unstructured.txt") as file:
    data = file.read()

# print(data) #1
#2
words = data.split()
# print(len(words))

# 3
# with open("unstructured.txt") as file:
#     lines = file.readlines()
# print(len(lines))

# 4
# word_to_be_checked = 'maintenance'
# if word_to_be_checked in data:
#     print(f"{word_to_be_checked} is present")

# 5
# print(data.lower().count('conveyor'))

# 6,7 printing lines with word "team" / "incident" in it
# with open("unstructured.txt") as file:
#     lines = file.readlines()
# for line in lines:
#     if "incident" in line:
#         print(line)

# 8
# with open("unstructured.txt") as file:
#     lines = file.readlines()
# for line in lines:
#     if "damaged" in line:
#         print(line)

#9
# with open("lowercase.txt",'w') as file:
#     file.write(data.lower())

# 10
dict_of_words = {"maintenance": 0  , "injuries":0 , "inspection":0 , "replacement": 0 , "operations" : 0}

for word in words:
    if "maintenance" in word:
        dict_of_words["maintenance"] += 1
    elif "injuries" in word:
        dict_of_words["injuries"] += 1
    elif "inspection" in word:
        dict_of_words["inspection"] += 1
    elif "replacement" in word:
        dict_of_words["replacement"] += 1
    elif "operations" in word:
        dict_of_words["operations"] += 1
for k,v in dict_of_words.items():
    print(k,v)