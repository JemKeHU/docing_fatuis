from fastapi import APIRouter, HTTPException, status
from schemas import ItemBase, ItemCreate, ItemChange

item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

items: list[ItemCreate] = []
UNIQUE_ID: int = 0

@item_router.get("")
async def get_items(limit: int = 10, offset: int = 0, keyword: str | None = None):
    filtered_items = []
    if keyword:
        for item in items:
            if keyword.lower() in item.name.lower():
                filtered_items.append(item)
    else:
        filtered_items = items
    return filtered_items[offset:offset + limit]

@item_router.get("/{item_id}")
async def get_item_by_id(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@item_router.post("")
async def post_item(item: ItemBase) -> ItemCreate:
    global UNIQUE_ID
    item_dict = item.model_dump()
    item_dict["id"] = UNIQUE_ID
    item_create = ItemCreate(**item_dict)
    items.append(item_create)
    UNIQUE_ID += 1
    return item_create

@item_router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def change_item_completely(item_id: int, new_item: ItemChange):
    for item in items:
        if item.id == item_id:
            item.name = new_item.name
            item.is_done = new_item.is_done
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@item_router.patch("/{item_id}/{is_done}")
async def change_done(item_id: int, is_done: bool):
    for item in items:
        if item.id == item_id:
            item.is_done = is_done
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            items.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")