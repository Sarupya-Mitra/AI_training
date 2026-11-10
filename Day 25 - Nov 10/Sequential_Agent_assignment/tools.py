from pathlib import Path
from agent_framework import tool
import json
import asyncio

DATA_PATH = Path(__file__).parent / "products.json"

def get_all_products():
    products = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return products

@tool
def search_products(topic : str)-> str:
    """Find products matching a name or category."""
    matches = []
    for product in get_all_products():
        if (topic.lower() in product["name"].lower()) or (topic.lower() in product['category'].lower()):
            matches.append(product)

    return json.dumps(matches)

@tool
def calculate_order_total(product_id : str,quantity : int) -> str:
    """Calculate total cost for a given quantity."""
    products = get_all_products()
    for product in products:
        if product["id"].lower() == product_id.lower():
            if quantity <= product["stock"]:
                return json.dumps({
                    "product" : product["name"],
                    "quantity" : quantity,
                    "Price_per_unit" : product["price_inr"],
                    "Total_price" : product["price_inr"] * quantity,
                    "currency" : "INR"
                })
            else:
                return "Product doesn't have enough stock"

    return "Product not found"

# async def main():
#     result = await search_products.invoke(
#         arguments={"topic": "laptop"}
#     )
#
#     for item in result:
#         print("Type:", type(item))
#         print("Object:", item)
#         print("Text:", getattr(item, "text", None))
#
# asyncio.run(main())