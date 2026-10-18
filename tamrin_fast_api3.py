from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# === مدل ورودی ===
class CreateUser(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=0, le=150)
    email: str

# === مدل خروجی (بدون email) ===
class UserResponse(BaseModel):
    name: str
    age: int

# === endpoint ===
@app.post("/users", response_model=UserResponse)
def create_user(user: CreateUser):
    # توی واقعیت اینجا کاربر رو توی دیتابیس ذخیره می‌کنیم
    return user   # ← FastAPI خودش email رو حذف می‌کنه