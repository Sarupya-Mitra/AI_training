import pandas as pd


with open("wildlife_report.txt") as f:
    text = f.read()

print(text) #1 Prints entire text
words = text.split()  # Get all the words

print(len(words)) #2 Count of all words

if "elephant" in text.lower():
    print("Elephant found") #3 Check if elephant is there or not

print(text.lower().count("elephant")) #4 Count the occurrences of "elephant"

with open("wildlife_report.txt") as f:
    lines = f.readlines()  # get all the lines in the txt file.
print("Printing lines with word trail:")  #5 Print lines with the word trail
for line in lines:
    if line.count("trail") > 0:
        print(line)

print("Printing lines with word animal:")  #6 Print lines with word animal
for line in lines:
    if line.count("animal") > 0:
        print(line)

