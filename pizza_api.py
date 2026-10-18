from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# دیکشنری پیتزاها
pizzas = {
    "margherita": 250000,
    "pepperoni": 300000,
    "veggie": 220000
}


# === ۱) GET /menu — لیست پیتزاها ===
@app.get("/menu")
def show_menu():
    return {"menu": list(pizzas.keys())}
    # list(pizzas.keys()) → ["margherita", "pepperoni", "veggie"]


# === ۲) GET /menu/{pizza_name} — اطلاعات یه پیتزا ===
@app.get("/menu/{pizza_name}")
def get_pizza(pizza_name: str):
    if pizza_name in pizzas:
        # اگه بود
        return {
            "name": pizza_name,
            "price": pizzas[pizza_name],
            "available": True
        }
    else:
        # اگه نبود
        return {"error": "pizza not found"}


# === ۳) GET /price — فیلتر قیمت ===
@app.get("/price")
def filter_price(max_price: int = 300000, size: str = "medium"):
    return {"max_price": max_price, "size": size}


# === ۴) POST /order — سفارش ===
class Order(BaseModel):
    pizza: str
    quantity: int
    address: str


@app.post("/order")
def place_order(order: Order):
    return {
        "message": f"{order.quantity}x {order.pizza} ordered to {order.address}",
        "status": "pending"
    }