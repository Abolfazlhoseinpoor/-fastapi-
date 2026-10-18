from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/search/{karbar}")
async def find_karbar(karbar: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"https://jsonplaceholder.typicode.com/users/{karbar}", timeout=10)
            response.raise_for_status() 
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="zaman tool keshid (timeout)")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"khata dar ertebat: {e}")           
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail="karbar peyda nashod")