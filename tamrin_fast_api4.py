from fastapi import FastAPI
from pydantic import BaseModel,Field
app = FastAPI()

class products(BaseModel):
    name : str = Field(min_length=2)
    price : int = Field(gt=0)
    quantity : int = Field(ge=0)

@app.post("/products")
def ajnas(product : products):
    return product