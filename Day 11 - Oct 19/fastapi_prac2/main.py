from fastapi import FastAPI,HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

def get_connection():
    conn = psycopg2.connect(host = "localhost",
    dbname = "library_store",user = "postgres",password = "Admin@123")

    return conn

class Book(BaseModel):
    book_id : int
    title : str
    author : str
    category : str
    price : float
    stock : int

# conn = get_connection()
# print("Connected to PostgreSQL successfully")

### 3. Inserting data
@app.post("/books")
def insert_books(book : Book):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("""INSERT INTO books values
    (%s,%s,%s,%s,%s,%s)""",(book.book_id,book.title,book.author,book.category,book.price,book.stock))

    conn.commit()
    curr.close()
    conn.close()
    return {
        "message" : "Book Added Successfully",
        "book" : book
    }

### 4. Reading all the data
@app.get("/books")
def get_books():
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("Select * from books")
    rows = curr.fetchall()

    if curr.rowcount == 0:
        curr.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    curr.close()
    conn.close()
    return {
        "message" : "Current Books in the library",
        "books" : rows
    }
### 5. Get books of a category
@app.get("/books/{category}")
def get_books_by_category(category : str):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("Select * from books where category = %s",(category,))
    rows = curr.fetchall()
    if curr.rowcount == 0:
        curr.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    curr.close()
    conn.close()
    return {"message": f"Books of the {category} category",
            "books" : rows}


### 6. books with a price threshold
@app.get("/books_price/{price}")
def get_books_with_price_greater_than_an_amount(price:float):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("Select * from books where price > %s",(price,))

    rows = curr.fetchall()
    if curr.rowcount == 0:
        curr.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    curr.close()
    conn.close()
    return {
        "message" : f"Books with price greater than {price}",
        "books" : rows
    }

### 7,8 Update a book
@app.put("/books/{book_id}")
def update_book(book_id :int, book : Book):
    conn = get_connection()
    curr = conn.cursor()

    curr.execute("""Update books set title = %s,author = %s , category = %s, price = %s, stock = %s 
     where book_id = %s""",(book.title,book.author,book.category,book.price,book.stock,book_id))

    if curr.rowcount == 0:
        curr.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")

    conn.commit()
    curr.close()
    conn.close()
    return {
        "message" : "Book Updated Successfully",
        "updated book" : book
    }
### 10
@app.delete("/books/{book_id}")
def delete_book(book_id :int):
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("""Delete from books where book_id = %s""",(book_id,))
    if curr.rowcount == 0:
        curr.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    conn.commit()
    curr.close()
    conn.close()
    return {
        "message" : "Book Deleted Successfully"
    }

### 13 Get max price book
@app.get("/books_max_price")
def get_max_book_price():
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("Select * from books order by price desc offset 0 limit 1")
    rows = curr.fetchall()
    return {
        "message" : f"Book(s) with maximum price in the library",
        "book" : rows
    }


### 14 Total stock of all books
@app.get("/books_stocks")
def get_all_book_stocks():
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("Select sum(stock) from books")

    rows = curr.fetchall()
    curr.close()
    conn.close()
    return {
        "message" : "Total stocks of books",
        "result" : rows
    }

### 15 Category wise books
@app.get("/category_wise_books")
def get_category_wise_books():
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("Select category,count(*) from books group by category")
    rows = curr.fetchall()

    curr.close()
    conn.close()
    return {
        "message" : "Category wise books",
        "result" : rows
    }

