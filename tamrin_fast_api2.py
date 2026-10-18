from fastapi import FastAPI
app = FastAPI()

@app.get("/product")
def search_bar(category : str = "all" , limit: int = 5):
    return {
        "category": category , "limit": limit
    }
    