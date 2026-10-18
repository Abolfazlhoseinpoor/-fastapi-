from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()

class Movie(BaseModel):
    title : str = Field(min_length=1)
    rating : float = Field(ge=0 , le=10)
    year : int = Field(ge=1900,le=2025)

@app.post("/movie")
def create_movie(movie : Movie):
    return movie