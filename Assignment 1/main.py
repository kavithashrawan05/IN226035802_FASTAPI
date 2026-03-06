from fastapi import FastAPI

app = FastAPI()


# 1st Question : Add 3 More Products

# Products List
products = [
    {"id": 1, "name": "Smartphone", "price": 15000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Headphones", "price": 2000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Coffee Maker", "price": 3500, "category": "Home Appliances", "in_stock": False},
    {"id": 4, "name": "Office Chair", "price": 7000, "category": "Furniture", "in_stock": True},

    # Newly Added Products
    {"id": 5, "name": "Laptop Stand", "price": 1200, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 4500, "category": "Accessories", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 3000, "category": "Electronics", "in_stock": False},
    {"id": 8, "name": "Wireless Mouse", "price": 800, "category": "Electronics", "in_stock": True}
]


# Endpoint to Get All Products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
    
    
    
# 2nd Question : Add a Category Filter Endpoint 


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = [
        product for product in products
        if product["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products,
        "total": len(filtered_products)
    }
    
    
# 3rd Question : Show only In-Stock Products

@app.get("/products/instock")
def get_instock_products():
    in_stock_products = [
        product for product in products
        if product["in_stock"] == True
    ]

    return {
        "in_stock_products": in_stock_products,
        "count": len(in_stock_products)
    }
    
    
# 4th Question : Build a store Info Endpoint

@app.get("/store/summary")
def get_store_summary():
    total_products = len(products)

    in_stock_count = len([
        product for product in products
        if product["in_stock"] == True
    ])

    out_of_stock_count = total_products - in_stock_count

    categories = list(set([
        product["category"] for product in products
    ]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }
    
    
# 5th Question : Search Products by name


@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    matched_products = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)
            
    if len(matched_products) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }
    
    
# Bonus : Cheapest Product


@app.get("/products/deals")
def get_product_deals():
    if not products:
        return {"message": "No products available"}

    cheapest_product = min(products, key=lambda product: product["price"])
    expensive_product = max(products, key=lambda product: product["price"])

    return {
        "best_deal": cheapest_product,
        "premium_pick": expensive_product
    }
    
    
    
