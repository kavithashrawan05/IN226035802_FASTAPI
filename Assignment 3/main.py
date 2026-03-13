
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]


# Q1 : Add two new products using POST 
class Product(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool


@app.post("/products", status_code=201)
def add_product(product: Product):

    # Check duplicate product name
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product with this name already exists")
        
    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }
    
    
# Q2 : Restock the USB Hub Using PUT

@app.put("/products/{product_id}")
def update_product(product_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):

    for product in products:
        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {
                "message": "Product updated",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")


# Q3 : Delete a Product and Handle Missing IDs

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": f"Product '{product['name']}' deleted"}

    raise HTTPException(status_code=404, detail="Product not found")


# Q4 : Build a Product Summary Dashboard

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
    

# Q5 : Build GET /products/audit — Inventory Summary

@app.get("/products/audit")
def products_audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["in_stock"]]
    in_stock_count = len(in_stock_products)

    out_of_stock_names = [p["name"] for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }
    
    
# Bonus Question : Apply a Category-Wide Discount

@app.get("/products/{product_id}")
def get_product(product_id: int):
    @app.put("/products/discount")
    def apply_discount(category: str, discount_percent: int):

        if discount_percent < 1 or discount_percent > 99:
            raise HTTPException(status_code=400, detail="Discount must be between 1 and 99")

        updated_products = []

        for product in products:
            if product["category"].lower() == category.lower():

                new_price = int(product["price"] * (1 - discount_percent / 100))
                product["price"] = new_price

                updated_products.append({
                    "name": product["name"],
                    "new_price": new_price
                })

            if not updated_products:
                return {"message": f"No products found in category '{category}'"}

        return {
        "updated_count": len(updated_products),
        "updated_products": updated_products
        }

