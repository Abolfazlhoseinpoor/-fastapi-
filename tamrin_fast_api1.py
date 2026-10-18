from fastapi import FastAPI
app = FastAPI()

@app.get("/user/{user_name}/{user_age}")
def sen(user_name : str, user_age : int):
    if user_age >= 18:
        status = "adult"
    else:
        status = "minor"

    return {
        "name":user_name , "age": user_age , "status": status
    }