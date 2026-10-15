# import fitz
import pymupdf

doc = pymupdf.open("EY_Digital_PDF_Practice.pdf")  # 1. Opening the pdf

# print(type(doc))
### 2 No. of pages
#print("No of pages : ", len(doc))

### 3 Extract only first page's text
# print(doc[0].get_text())

### 4 Extracting text from all pages
# for page in doc:
#     print(page.get_text())

### 5 Searching for a word
# word_to_search = "maintenance"
# for page_num in range(len(doc)):
#     page = doc[page_num]
#     matches = page.search_for(word_to_search)
#     if matches:
#         print(f"Word {word_to_search} found {len(matches)} matches in page no. {page_num + 1}")

### 6. Counting the occurrence of a word
# word_to_search = "V303"
# count = 0
# for page in doc:
#     matches = page.search_for(word_to_search)
#     count = count + len(matches)
# print(f"Word  {word_to_search} has {count} appearances")

### 7. Extract only page 2's text
# print(doc[1].get_text())

### 8. 8. writing all the extracted text to a file
with open("digital_pdf_text.txt",'a') as f:
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        f.write(f"---------- Page : {page_num + 1} ----------\n")
        f.write(text)
f.close()