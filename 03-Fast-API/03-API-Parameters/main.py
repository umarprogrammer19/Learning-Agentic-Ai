from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

# Call the Fast Api
app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

# Get route
@app.get("/")
async def main():
    return {"message": "I am Learning Path Patameters"}


# For getting items by if the id is path parameter
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,  # Means the parameter is required
        title="The Id Of The Item",
        description="A unique identifier for the item",
        ge=1,  # greater then equal to 1
    )
):
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(
    q: str | None = Query(
        None,  # for optional parameter default value is None
        title="Query String",
        description="Query string for searching items",
        min_length=3,
        max_length=50,
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),  # Less than or equal to 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.put("/items/validated/{item_id}")
async def update_items(
    item_id: int = Path(..., title="Item Id", ge=1),
    q: str | None = Query(None, min_length=3),
    item: Item | None = Body(None, desciption="Optional Item Data (JSON BODY)"),
):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item.model_dump()})
    return result
