from fastapi import FastAPI
from pydantic import BaseModel,Field
app = FastAPI()

class Comment(BaseModel):
    author : str = Field(min_length=1,max_length=30)
    text : str = Field(min_length=1,max_length=500)

class Post(BaseModel):
    title : str = Field(min_length=1,max_length=100)
    content : str = Field(min_length=10)
    tags : list[str]
    published : bool = True
    comments : list[Comment] = []


class Post_response(BaseModel):
    title : str
    tags : list[str]    
    published : bool

@app.post("/posts",response_model=Post_response)
def body(post:Post):
    return post