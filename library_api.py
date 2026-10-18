from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

book = {
    "python": {"author": "Ali", "year": 2020},
    "fastapi": {"author": "Sara", "year": 2022},
    "javascript": {"author": "Reza", "year": 2019}
}
# normal fast api
@app.get("/books")
def get_book():
    return {"books":list(book.keys())}


#path fastapi
@app.get("/books/{books_name}")
def one_get_book(books_name : str):
    if books_name in book:
        return {
            "title": books_name, 
            "author": book[books_name]["author"], 
            "year": book[books_name]["year"], 
            "available": True
            }
    else:
        return {
            "errors":"books not found!!"
        }

# quary fast api
@app.get("/search")
def filter_search(author : str = "all", year : int = 2024 ):
    return {
        "author":author,
        "year":year 
    }


# body post fast api (docks)
class ketab(BaseModel):
    books_name : str
    user : str
    days : int

@app.post("/sefaresh")
def sefaresh(sefaresh : ketab):
    return {
        "message": f"{sefaresh.books_name} borrowed by {sefaresh.user} for {sefaresh.days}",
        "status": "success"
    }