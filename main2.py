from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# In-memory "dataset"
db: dict[int, dict] = {
    1: {"name": "apple", "price": 1.25, "is_offer": False},
    2: {"name": "banana", "price": 0.75, "is_offer": True},
    3: {"name": "milk", "price": 3.49, "is_offer": None}, 
}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "count": len(db)}
    )


# ---- Read all (simple list) ----
@app.get("/items")
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """
    Return items as a list, with basic pagination.
    """
    all_items = [{"id": item_id, **item} for item_id, item in sorted(db.items())]
    return {
        "count": len(all_items),
        "items": all_items[skip : skip + limit],
    }


# ---- Read one by ID ----
@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    Return a single item by its ID.
    """
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **db[item_id]}


# ---- Add data  ----
@app.post("/items", status_code=201)
def create_item(item: Item):
    """
    Insert a new item into the in-memory dataset.
    """
    next_id = (max(db.keys()) + 1) if db else 1
    db[next_id] = item.model_dump()
    return {"message": "Item stored", "id": next_id, "item": db[next_id]}


# ---- Simple "search" example ----
@app.get("/search")
def search_items(
    q: str = Query(..., min_length=1),
    offer_only: bool = False,
):
    """
    Very simple search by substring in name.
    """
    q_lower = q.lower()
    results = []
    for item_id, item in db.items():
        if q_lower in item["name"].lower():
            if offer_only and item.get("is_offer") is not True:
                continue
            results.append({"id": item_id, **item})
    return {"count": len(results), "items": results}