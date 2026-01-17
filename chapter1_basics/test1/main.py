from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def test1():
    return {"message":"hello"}