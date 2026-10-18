from fastapi import FastAPI
from pydantic import BaseModel,Field
app = FastAPI()

class Author(BaseModel):
    name : str = Field(min_length=2)
    country : str

class Book(BaseModel):
    title : str
    year : int = Field(ge= 1900 , le= 2026)
    author : Author

@app.post("/book")
def create_book_endpoint(book:Book):
    return book