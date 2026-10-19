from flask import Flask,jsonify
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#     return "Hello from flask"
#
# @app.route("/about")
# def about():
#     return "About Page"
#
# @app.route("/home/<name>")
# def say_hello(name):
#     return f"Hello {name}"


app = Flask(__name__)

@app.route("/products")
def get_products():
    products = [
        {"id": 1, "name": "Keyboard", "price": 2500},
        {"id": 2, "name": "Monitor", "price": 12000}
    ]

    return jsonify(products)


@app.route("/products/<int:product_id>")
def get_product(product_id):
    products = [
        {"id": 1, "name": "Keyboard", "price": 2500},
        {"id": 2, "name": "Monitor", "price": 12000}
    ]

    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"message": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)