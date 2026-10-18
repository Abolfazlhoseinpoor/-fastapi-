import asyncio
import httpx
from fastapi import FastAPI,HTTPException

app = FastAPI()

async def user():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users/1",timeout=10)
        response.raise_for_status
        data = response.json()
        return data

async def post():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts/1",timeout=10)
        response.raise_for_status
        data = response.json()
        return data

@app.get("/compare")
async def compare():
    try:
        user_data = await asyncio.gather(user())
        post_data = await asyncio.gather(post())
        print(user_data)
        return {
            "user_name": user_data["name"],
            "post_title": post_data["title"]
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504,detail="time out")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500,detail=f"error koly {e}")