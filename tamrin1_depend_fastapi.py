from fastapi import FastAPI,Depends
app = FastAPI()

def get_app_config():
    return {"app_name": "My Agent", "version": "1.0"}
@app.get("/config")
def config(msg : dict = Depends(get_app_config)):
    return msg