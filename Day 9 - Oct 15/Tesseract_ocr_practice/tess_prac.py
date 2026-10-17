import pymupdf
import pytesseract
from PIL import Image

### 1. Opening doc
doc = pymupdf.open("EY_Scanned_PDF_OCR_Practice.pdf")

### 2. Converting pdf to image
page = doc[0]
pix = page.get_pixmap()
pix.save("scanned_page.png")
image = Image.open("scanned_page.png")

### 3. Run Tesseract OCR on the image
text = pytesseract.image_to_string(image)
# print(text)

### 5. Searching for a word
# word_to_Search = "Forklift FL-17"
# if word_to_Search in text:
#     print(f"{word_to_Search} is present")
# else:
#     print(f"{word_to_Search} is absent")

### 6. Searching for word
# word_to_Search = "injuries"
# if word_to_Search in text:
#     print(f"{word_to_Search} is present")
# else:
#     print(f"{word_to_Search} is absent")

### 7. Printing lines with a particular word
# word_to_search = "inspection"
# lines = text.splitlines()
# clean_lines = [line.strip() for line in lines if line.strip()]
# for line in clean_lines:
#     if word_to_search in line:
#         print(line)

### 8
# with open("ocr_result.txt", "a") as file:
#     file.write(text)

### 9 Counting the occurrance of a word
# word_to_search = "inspection"
# count = text.lower().count(word_to_search)
# print(count)

### 10. Print lines containing a certain word
word_to_search = "Loading Bay"
lines = text.splitlines()
for line in lines:
    if word_to_search in line:
        print(line)

### Extra for debugging
# with open("ocr_result.txt") as f:
#     data = f.readlines()
# for line in data:
#     if word_to_search in line:
#         print(line)