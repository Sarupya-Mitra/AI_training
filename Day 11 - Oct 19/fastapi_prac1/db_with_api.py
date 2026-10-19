from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id : int
    name : str
    price : float

def get_db_connection():
    conn = psycopg2.connect(host="localhost",
                            database="fastapi_store",
                            user="postgres", password="Admin@123")

    print("DB Connected")
    return conn

# conn = get_db_connection()
# conn.close()

@app.get("/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("Select * from products")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

@app.post("/products")
def create_product(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""Insert into products values(%s,%s,%s)""",
                   (product.id,product.name,product.price))

    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message" : "product added",
        "product" : product
    }

@app.get("/products/{product_id}")
def get_product_by_id(product_id : int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"Select * from products where id = {product_id}")
    rows = cursor.fetchall()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message": "Product found",
        "product" : rows
    }

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""Update products set name = %s,
    price = %s where id = %s""",(product.name,product.price,product_id))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message" : "Product Updated",
        "product" : product
    }

@app.delete("/products/{product_id}")
def delete_product(product_id : int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""Delete from products where id= %s""",
                   (product_id))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")

    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message": "Product deleted"
    }
