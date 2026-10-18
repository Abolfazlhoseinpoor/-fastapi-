import asyncio , httpx
from fastapi import FastAPI,HTTPException,Depends

app = FastAPI()

async def get_http():
    async with httpx.AsyncClient() as client:
        yield client
async def get_user_info(user_id : int, client : httpx.AsyncClient):
    response = await client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}" , timeout= 10)
    response.raise_for_status()
    data = response.json()
    return data
async def get_user_post(user_id : int,client:httpx.AsyncClient):
    response = await client.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}",timeout=10)
    response.raise_for_status()
    data = response.json()
    return data
async def get_user_todo(user_id : int,client : httpx.AsyncClient):
    response = await client.get(f"https://jsonplaceholder.typicode.com/todos?userId={user_id}",timeout=10)
    response.raise_for_status()
    data = response.json()
    return data
@app.get("/agent/profile/{user_id}")
async def show_user(user_id:int,client: httpx.AsyncClient = Depends(get_http)):
    user_info,user_post,todo_data = await asyncio.gather(
        get_user_info(user_id,client),
        get_user_post(user_id,client),
        get_user_todo(user_id,client)
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

    
