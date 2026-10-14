import pandas as pd

with open("file.txt") as f:
    text = f.read()

print(text)

words = text.split()
# Total words
print(len(words))

# Searching a word
if "vibration" in text.lower():
    print("Found vibration")

# Counting the occurance of a word
print(text.lower().count("vibration"))