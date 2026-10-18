import asyncio , httpx
from fastapi import FastAPI,Request,HTTPException,BackgroundTasks,Depends
from pydantic import BaseModel,Field
import time


app = FastAPI(title="mini project fastapi")

@app.middleware("http")
async def gurd(request : Request , next):
    start = time.time()
    print(f"masir: {request.url.path}")
    response = await next(request)
    zaman = time.time() - start
    response.headers["X-Process-Time"] = str(zaman)
    return response

class Book_create(BaseModel):
    title : str = Field(min_length=2)
    author : str = Field(min_length=3)

class Book_response(BaseModel):
    id : int
    title : str
    author : str
    available : bool = True

books_db = {
    1: {"title": "Python 101", "author": "Ali", "available": True},
    2: {"title": "FastAPI Guide", "author": "Sara", "available": False}
}

def get_book_or_404(id : int):
    if id not in books_db:
        raise HTTPException(status_code=404,detail="book not found!")
    return books_db[id]

def log(title : str):
    time.sleep(2)
    print(f"title zakhire shod : {title}")

async def user_info(client : httpx.AsyncClient):
    response = await client.get("https://jsonplaceholder.typicode.com/users/1",timeout=20)
    response.raise_for_status()
    data = response.json()
    return data

async def todo_info(client :httpx.AsyncClient):
    response  = await client.get("https://jsonplaceholder.typicode.com/todos/1",timeout=20)
    response.raise_for_status()
    data = response.json()
    return data

@app.get("/book",response_model=dict[int,Book_response])
def show_book():
    return books_db

@app.get("/book/{book_id}",response_model=Book_response)
def show_id_book(book : dict = Depends(get_book_or_404)):
    return book

@app.post("/books",status_code=201,response_model=Book_response)
def create_book(book : Book_create ,back_task : BackgroundTasks ):
    new = max(books_db.keys()) +1
    new_book = {"title":book.title,"author":book.author}
    books_db[new] = new_book
    back_task.add_task(log,book.title)
    return {"id": new, **new_book}

@app.delete("/tasks/{book_id}")
def delete_task(book : dict = Depends(get_book_or_404), book_id : int = None):
    del books_db[book_id]
    return {"message": f"Task {book_id} deleted successfully"}

@app.put("/tasks/{book_id}/complete", response_model=Book_response)
def complete_task(book: dict = Depends(get_book_or_404), book_id: int = None):
    book["available"] = True
    return {"id": book_id, **book}


@app.get("/tasks/{book_id}/external-info")
async def get_external_info(book: dict = Depends(get_book_or_404), book_id: int = None):
    async with httpx.AsyncClient(timeout=10) as client:
        user_data, todo_data = await asyncio.gather(
            user_info(client),
            todo_info(client)
        )
        
        return {
            "book_title":book["title"],
            "borrowed_by": user_data["name"],
            "task_status": todo_data["title"]
        }
