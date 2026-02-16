# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"} 

@app.get("/items/")
async def read_items():
    return {"message": "hello"}

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"message": "Item received successfully!", "item": item}












"""
from fastapi.responses import JSONResponse

@app.get("/items/")
async def read_items():
    return JSONResponse(content={"message": "hello"}, status_code=400)
"""