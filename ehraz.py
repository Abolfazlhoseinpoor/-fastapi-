from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import uuid

app = FastAPI(title="ehraz hoviyat")
api_key = APIKeyHeader(name="token!!", auto_error=False) 
user_data = {}

class SignUpModel(BaseModel):
    username: str
    password: str
class SignInModel(BaseModel):
    username: str
    password: str

def user_token(token: str = Depends(api_key)):
    if not token:
        raise HTTPException(status_code=401, detail="shoma token nadarid!")
    for username, data in user_data.items():
        if data["token"] == token:
            return username
    raise HTTPException(status_code=401, detail="token eshtebah!!")

@app.post("/sign_up")
def sign_up(user: SignUpModel):
    if user.username in user_data:
        raise HTTPException(status_code=400, detail="in karbar vojod darad")
    
    user_data[user.username] = {"password": user.password, "token": None}
    return {"message": "Sabt nam ba movafaghiat anjam shod!"}

@app.post("/sign_in")
def sign_in(user: SignInModel):
    if user.username not in user_data:
        raise HTTPException(status_code=404, detail="in karbar peyda nashod")   
    if user_data[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="ramz eshtebah ast!")

    token_jadid = str(uuid.uuid4())
    user_data[user.username]["token"] = token_jadid
    return {
        "message": "shoma ba movafaghiyat sign_in kardid!",
        "token": token_jadid
    }

@app.get("/hesab")
def hesab(username: str = Depends(user_token)):
    return {
        "message": f"khosh amadid {username} in safe hesab shomast!"
    }

@app.middleware("http")
async def guard(request: Request, call_next):
    public = ["/sign_in", "/sign_up", "/docs", "/openapi.json"]
    
    if request.url.path not in public:
        token = request.headers.get("token!!")
        etebar = False
        for data in user_data.values():
            if data["token"] is not None and data["token"] == token:
                etebar = True
                break
        if not etebar:
            return JSONResponse(status_code=401, content={"message": "shoma dastrasi nadarid!"})
            
    response = await call_next(request)
    return response