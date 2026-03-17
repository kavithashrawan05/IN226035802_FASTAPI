-----------------------------------------------------------------------Day - 5 ------------------------------------------------------------------

from fastapi import FastAPI, HTTPException

app = FastAPI()

# ---------------------------------------
# Products Database
# ---------------------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# ---------------------------------------
# Q1 – Search Products
# ---------------------------------------
@app.get("/products/search")
def search_products(keyword: str):

    results = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            results.append(product)

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "results": results,
        "total_found": len(results)
    }


# ---------------------------------------
# Q2 – Sort Products
# ---------------------------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# ---------------------------------------
# Q3 – Pagination
# ---------------------------------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    total_products = len(products)
    total_pages = (total_products + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_products = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": paginated_products
    }


# ---------------------------------------
# Q4 – Sort by Category then Price
# ---------------------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(products, key=lambda x: (x["category"], x["price"]))

    return {
        "products": sorted_products
    }


# ---------------------------------------
# Q5 – Orders Database
# ---------------------------------------
orders = []

@app.post("/orders")
def create_order(customer_name: str, product_id: int, quantity: int):

    for product in products:
        if product["id"] == product_id:

            order = {
                "order_id": len(orders) + 1,
                "customer_name": customer_name,
                "product_name": product["name"],
                "quantity": quantity,
                "total_price": product["price"] * quantity
            }

            orders.append(order)

            return {
                "message": "Order placed successfully",
                "order": order
            }

    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/orders/search")
def search_orders(customer_name: str):

    results = []

    for order in orders:
        if customer_name.lower() in order["customer_name"].lower():
            results.append(order)

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# ---------------------------------------
# Q6 – Browse (Search + Sort + Pagination)
# ---------------------------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    filtered_products = products

    # Filter by keyword
    if keyword:
        filtered_products = [
            p for p in filtered_products
            if keyword.lower() in p["name"].lower()
        ]

    # Sort
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False
    filtered_products = sorted(filtered_products, key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_found = len(filtered_products)
    total_pages = (total_found + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_products = filtered_products[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated_products
    }


# ---------------------------------------
# Get Product by ID (MUST BE LAST)
# ---------------------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


# ---------------------------------------
# BONUS – Paginate Orders
# ---------------------------------------
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    total_orders = len(orders)
    total_pages = (total_orders + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_orders = orders[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": paginated_orders
    }
