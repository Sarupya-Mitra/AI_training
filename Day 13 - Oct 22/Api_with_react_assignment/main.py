import psycopg2
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware


# def insert_data():
#     cursor = conn.cursor()
#     cursor.execute("""CREATE TABLE products (
#     id INT PRIMARY KEY,
#     name VARCHAR(100),
#     price DECIMAL(10,2),
#     image VARCHAR(500)
#     ); """)
#     cursor.close()
#     conn.commit()
#     conn.close()



app = FastAPI()

# Enable CORS for React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5173/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection_db():
    conn = psycopg2.connect(host = "localhost",
                        user="postgres",
                        dbname = "product_store",
                        password = "Admin@123")
    return conn

@app.get("/products")
def get_products():
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    products = []
    for row in rows:
        products.append({
            "id" : row[0],
            "name" : row[1],
            "price" : row[2],
            "image" : row[3]
        })
    return products

@app.post("/products")
def insert_products(product: dict):
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (id,name, price, image) VALUES (%s, %s, %s,%s)",
                   (product["id"] , product["name"], product["price"],product["image"]))
    conn.commit()
    cursor.close()
    conn.close()
    return product

@app.put("/products/{product_id}")
def update_products(product_id: int, product: dict):
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s, image = %s WHERE id = %s",
                   (product["name"], product["price"], product["id"], product_id))
    conn.commit()
    cursor.close()
    conn.close()

@app.delete("/products/{product_id}")
def delete_product(product_id : int):
    conn = get_connection_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s",(product_id,))
    conn.commit()
    cursor.close()
    conn.close()


# if __name__ == "__main__":
