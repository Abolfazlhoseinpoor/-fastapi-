from fastapi import FastAPI,Depends
app = FastAPI()

def verify_api_key():
    return "secret123"
@app.get("/secure-data/{password}")
def ramz(password : str = Depends(verify_api_key)):
    if password  == "secret123":
        return {"status": "access granted"}
    else:
        return {"status": "deaccess granted"}