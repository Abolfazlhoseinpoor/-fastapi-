from fastapi import FastAPI, HTTPException

app = FastAPI()

products = {
    1: {"name": "Laptop", "price": 25000000, "stock": 5},
    2: {"name": "Phone", "price": 15000000, "stock": 0},
    3: {"name": "Tablet", "price": 8000000, "stock": 12}
}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product peyda nashod!")
    return products[product_id]

@app.get("/products/{product_id}/buy")
def buy_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product peyda nashod!")
    if products[product_id]["stock"] == 0:
        raise HTTPException(status_code=400, detail="Out of stock")
    return {
        "message": f"Bought {products[product_id]['name']}",
        "remaining": products[product_id]["stock"] - 1
    }