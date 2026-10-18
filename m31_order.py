from fastapi import FastAPI,BackgroundTasks
import time

app = FastAPI()


def send_order_invoice(order_id : int , email : str):

    time.sleep(3)
    print(f"shomare factor {order_id} be email : {email} send shod!!")

@app.post("/checkout")
def order(order_id : int,email : str,back_tast : BackgroundTasks):
    back_tast.add_task(send_order_invoice,order_id,email)
    return {
        "status": "success", "message": "factor sabt shod!."
        }
