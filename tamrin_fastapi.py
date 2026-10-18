from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from pydantic import BaseModel, Field
import time
import asyncio
import httpx

app = FastAPI(title="Final Task Manager")

# === ۱. MIDDLEWARE (زمان‌سنج) ===
@app.middleware("http")
async def time_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# === ۲. دیتابیس قلابی ===
tasks_db = {
    1: {"title": "Learn FastAPI", "completed": False},
    2: {"title": "Build an Agent", "completed": True}
}

# === ۳. مدل‌های Pydantic ===
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

# === ۴. Background Task ===
def log_task_creation(title: str):
    time.sleep(2)
    print(f"📝 لاگ پس‌زمینه: تسک '{title}' ساخته شد.")

# === ۵. Dependency ===
def get_task_or_404(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

# === ۶. توابع Async برای اتصال به API خارجی ===
async def fetch_user_info(client: httpx.AsyncClient):
    res = await client.get("https://jsonplaceholder.typicode.com/users/1")
    return res.json()

async def fetch_random_post(client: httpx.AsyncClient):
    res = await client.get("https://jsonplaceholder.typicode.com/posts/1")
    return res.json()

# ==========================================
#                   ENDPOINTS
# ==========================================

@app.get("/tasks", response_model=dict[int, TaskResponse])
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task: dict = Depends(get_task_or_404), task_id: int = None):
    return task

@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, background_tasks: BackgroundTasks):
    new_id = max(tasks_db.keys()) + 1
    new_task = {"title": task.title, "completed": False}
    tasks_db[new_id] = new_task
    background_tasks.add_task(log_task_creation, task.title)
    return {"id": new_id, **new_task}

@app.put("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task: dict = Depends(get_task_or_404), task_id: int = None):
    task["completed"] = True
    return {"id": task_id, **task}

@app.delete("/tasks/{task_id}")
def delete_task(task: dict = Depends(get_task_or_404), task_id: int = None):
    del tasks_db[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

# 👇 اینجا جادوی ASYNC و HTTPX رو می‌بینی 👇
@app.get("/tasks/{task_id}/external-info")
async def get_external_info(task: dict = Depends(get_task_or_404), task_id: int = None):
    async with httpx.AsyncClient(timeout=10) as client:
        # هر دو درخواست رو همزمان می‌فرستیم
        user_data, post_data = await asyncio.gather(
            fetch_user_info(client),
            fetch_random_post(client)
        )
        
        return {
            "task_title": task["title"],
            "assigned_user": user_data["name"],
            "related_post": post_data["title"]
        }