import asyncio
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()


async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}", timeout=10)
        response.raise_for_status()  
        return response.json()

@app.get("/users")
async def get_users():
    try:
        tasks = [get_user(1), get_user(2), get_user(3)]
        users_data = await asyncio.gather(*tasks)        
        names = []
        for user in users_data:
            names.append(user["name"])
            
        return names   
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="time out")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"khataye koly: {e}")