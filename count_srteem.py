import asyncio 
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
app = FastAPI()

async def my_generator():
    for i in range(1, 6):
        yield str(i) + " "
        await asyncio.sleep(1)

@app.get("/count-stream")
async def count_stream():
    return StreamingResponse(my_generator(), media_type="text/plain") 