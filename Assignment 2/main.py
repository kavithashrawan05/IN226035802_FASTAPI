from pydantic import BaseModel, Field
from typing import Optional
from typing import List 

from fastapi import FastAPI

app = FastAPI()


# Question 1 : Filter Products by Minimum Price

products = [
    {"id" : 1,"name": "Wireless Mouse", "category": "electronics", "price": 499, "in_stock" : True},
    {"id" : 2,"name": "USB Hub", "category": "electronics", "price": 799, "in_stock" : True},
    {"id" : 2,"name": "Notebook", "category": "stationery", "price": 50, "in_stock" : False},
    {"id" : 2,"name": "Pen Set", "category": "Stationery", "price": 49, "in_stock" : True}
]

feedback = []


@app.get("/products/filter")
def filter_products(category: str = None, min_price: int = None, max_price: int = None):
    result = products

    if category:
        result = [p for p in result if p["category"] == category]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    return result


# Q2 : Get Only the Price of a Product


@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }
    
    return {"error": "Product not found"}

# Q3 :

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)
    
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
}
    
# Q4 :


@app.get("/products/summary")
def product_summary():
    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = len([p for p in products if not p["in_stock"]])

    most_expensive = max(products, key=lambda x: x["price"])
    cheapest = min(products, key=lambda x: x["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }
    
    
# Q5 :

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)
    
    
class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)
    
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }
    
    
# Bonus Point Question : 

orders = []

class Order(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)
    
    
@app.post("/orders")
def create_order(order: Order):
    new_order = order.dict()
    new_order["id"] = len(orders) + 1
    new_order["status"] = "pending"

    orders.append(new_order)

    return new_order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["id"] == order_id:
            return order

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["id"] == order_id:
            order["status"] = "confirmed"
            return order

    return {"error": "Order not found"}
