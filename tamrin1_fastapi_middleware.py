from fastapi import FastAPI,Request
import time
app = FastAPI()

@app.middleware("http")
async def time_miidleware(request:Request,call_next):
    start =  time.time()
    print(f"masir : {request.url.path}")
    response = await call_next(request)
    end = time.time()
    procces = start - end
    response.headers["X-procces-time"] = str(procces)
    return response

@app.get("/admins")
def admins():
    return{"page":"admins"}
@app.get("/home")
def home():
    return{"page":"home"}
@app.get("/slow")
def slow():
    time.sleep(1)
    return{"message":"in yek endpoint slow!!"}