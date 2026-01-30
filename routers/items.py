from fastapi import APIRouter, HTTPException, status
from schemas.items import ItemCreate, ItemPut, ItemPatch, ItemRead
from database import SessionDep
from rep import ItemRepository

item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@item_router.get("", response_model=list[ItemRead])
async def get_items(session: SessionDep):
    return await ItemRepository.get_all_items(session)

@item_router.post("", response_model=ItemRead)
async def post_item(item_create: ItemCreate, session: SessionDep):
    item = await ItemRepository.add_item(item_create, session)
    return item

@item_router.get("/{item_id}", response_model=ItemRead)
async def get_item_by_id(item_id: int, session: SessionDep):
    item = await ItemRepository.get_by_id(item_id, session)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found"
        )
    return item

@item_router.put("/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemRead)
async def change_item_completely(item_id: int, new_item: ItemPut, session: SessionDep):
    item = await ItemRepository.get_by_id(item_id, session)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return await ItemRepository.put_item(item, new_item, session)

@item_router.patch("/{item_id}", response_model=ItemRead)
async def patch_item(item_id: int, item_patch: ItemPatch, session: SessionDep):
    item = await ItemRepository.get_by_id(item_id, session)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return await ItemRepository.patch_item(item, item_patch, session)

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(item_id: int, session: SessionDep):
    deleted = await ItemRepository.delete_item(item_id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )