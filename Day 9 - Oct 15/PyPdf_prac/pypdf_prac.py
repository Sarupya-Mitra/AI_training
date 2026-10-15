from pypdf import PdfReader

### 1. Opening the pdf
reader = PdfReader('EY_Digital_PDF_Practice.pdf')


### 2. Print no of pages
# print("Pages:",len(reader.pages))

### 3. Extract text from first page
# print("First page text : \n",reader.pages[0].extract_text())

### 4. Extract text from 2nd page
# print("First page text : \n",reader.pages[1].extract_text())

### 5. Combine both pages into a string
# all_text = ""
# for page in reader.pages:
#     text = page.extract_text()
#     all_text += text
# print(all_text)

### 6. Searching for a word
# word_to_search = "NorthStar Maintenance"
# count = 0
# for i,page in enumerate(reader.pages):
#     text = page.extract_text()
#     if word_to_search in text:
#         count = text.lower().count(word_to_search.lower())
#     print(f"Page {i+1} has {count} no of matches for the word \'{word_to_search}\'")
#     count = 0

### 7. Counting occurrences of a word
# word_to_search = "vendor"
# count = 0
# for i,page in enumerate(reader.pages):
#     text = page.extract_text()
#     if word_to_search.lower() in text.lower():
#         count = text.lower().count(word_to_search.lower())
#     print(f"Page {i+1} has {count} no of matches for the word \'{word_to_search}\'")
#     count = 0

### 8 Saving the extracted text in a different file
with open("pypdf_output_text.txt", "a") as file:
    for i,page in enumerate(reader.pages):
        text = page.extract_text()
        file.write(f"---------- Page {i+1} ----------\n")
        file.write(text)
file.close()