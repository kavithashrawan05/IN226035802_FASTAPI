-------------------------------------------------------Day - 4 ---------------------------------------------------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# Question : 1 Add Items to the Cart

# Products list (with IDs)
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# Order list
orders = []
# Cart list
cart = []


cart = []

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail="Product out of stock")

    # check if product already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            subtotal = item["quantity"] * product["price"]

            return {
                "message": "Cart updated",
                "cart_item": {
                    "product_id": product_id,
                    "product_name": product["name"],
                    "quantity": item["quantity"],
                    "unit_price": product["price"],
                    "subtotal": subtotal
                }
            }

    subtotal = quantity * product["price"]

    cart_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"]
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": {
            **cart_item,
            "subtotal": subtotal
        }
    }



@app.get("/cart")
def view_cart():

    item_count = len(cart)
    grand_total = sum(item["quantity"] * item["unit_price"] for item in cart)

    return {
        "items": cart,
        "item_count": item_count,
        "grand_total": grand_total
    }


@app.delete("/cart/remove/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not in cart")

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    customer_name = data.customer_name
    delivery_address = data.delivery_address

    order = {
        "order_id": len(orders) + 1,
        "customer_name": customer_name,
        "delivery_address": delivery_address,
        "items": cart.copy(),
        "total_amount": sum(item["unit_price"] * item["quantity"] for item in cart)
    }

    orders.append(order)
    cart.clear()

    return {
        "message": "Order placed",
        "orders_placed": len(orders),
        "grand_total": order["total_amount"]
    }


@app.get("/orders")
def get_all_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }



