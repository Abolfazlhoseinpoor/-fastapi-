import asyncio,httpx
from fastapi import FastAPI
app = FastAPI()

async def get_user_info(user_id : int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}" , timeout= 10)
        response.raise_for_status()
        data =response.json()
        return data
async def get_user_post(user_id : int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}",timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
async def get_user_todo(user_id : int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://jsonplaceholder.typicode.com/todos?userId={user_id}",timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
@app.get("/agent/profile/{user_id}")
async def show_info(user_id:int):
    user_info,user_post,todo_data = await asyncio.gather(
        get_user_info(user_id),
        get_user_post(user_id),
        get_user_todo(user_id)
    )
    complete = 0
    for todo in todo_data:
        if todo["completed"] == True:
            complete += 1
    return {
        "agent_report" : {"username":user_info["name"],
        "email":user_info["email"],
        "post_totall": len(user_post),
         "completed_todos":complete}
    }