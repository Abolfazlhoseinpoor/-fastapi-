from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def fake_ai_stream():
    words = ["Salam", " man", " yek", " AI", " agent", " hastam", " ke", " kalame", " be", " kalame", " javab", " midam."]
    
    for word in words:
        yield word + " "      
        await asyncio.sleep(0.5) 

@app.get("/chat/stream")
def chat_stream():
    return StreamingResponse(fake_ai_stream(), media_type="text/plain")