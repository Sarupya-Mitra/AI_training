from multiprocessing.managers import rebuild_as_list

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Products(BaseModel):
    id : int
    name: str
    price: float

products = []

@app.get("/")
def home():
    return {"message" : "Welcome to Products Page"}

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def add_products(product: Products):
    products.append(product)
    return {
        "message" : "Product added",
        "product" : product
    }

@app.get("/products/{id}")
def get_product_by_id(id : int):
    for product in products:
        if product.id == id:
            return {
                "message" : "Product found",
                "product" : product
            }
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Products):
    for index,product in enumerate(products):
        if product.id == product_id:
            products[index] = updated_product
            return {
                "message" : "Product updated",
                "product" : product
            }
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{prod_id}")
def deleted_product(prod_id : int):
    for index, product in enumerate(products):
        if prod_id == product.id:
            products.pop(index)
            return {"message" : "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")