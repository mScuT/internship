from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id, get_item_by_id
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items(
    min_price: float = Query(0.0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100)
) -> list[Item]:
    return get_items(min_price=min_price, skip=skip, limit=limit)



@app.post("/items")
def add_item(item: ItemCreate) -> Item:
    return create_item(item)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate) -> Item:
    existing = get_item_by_id(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated = update_item_by_id(item_id, item)
    if not updated:
        raise HTTPException(status_code=422, detail="Duplicate item name")

    return updated

