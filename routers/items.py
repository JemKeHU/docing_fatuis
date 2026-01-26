from fastapi import APIRouter, HTTPException, status
from schemas.items import ItemBase, ItemCreate, ItemPut, ItemPatch
from models.items import ItemModel
from database import SessionDep
from sqlalchemy import select, delete
from sqlalchemy.engine import CursorResult
from typing import cast

item_router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

@item_router.get("")
async def get_items(session: SessionDep):
    query = select(ItemModel)
    result = await session.execute(query)
    return result.scalars().all()

@item_router.post("", response_model=ItemCreate)
async def post_item(item: ItemBase, session: SessionDep):
    new_item = ItemModel(
        name=item.name
    )
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item

@item_router.get("/{item_id}")
async def get_item_by_id(item_id: int, session: SessionDep):
    query = select(ItemModel).where(ItemModel.id == item_id)
    result = await session.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item not found"
        )
    return item

@item_router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def change_item_completely(item_id: int, new_item: ItemPut, session: SessionDep):
    query = select(ItemModel).where(ItemModel.id == item_id)
    result = await session.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    item.name = new_item.name
    item.is_done = new_item.is_done
    await session.commit()
    await session.refresh(item)
    return item

@item_router.patch("/{item_id}")
async def change_done(item_id: int, item_patch: ItemPatch, session: SessionDep):
    query = select(ItemModel).where(ItemModel.id == item_id)
    result = await session.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updates = item_patch.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item

@item_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(item_id: int, session: SessionDep):
    query = delete(ItemModel).where(ItemModel.id == item_id)
    result = await session.execute(query)
    result = cast(CursorResult, result)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    await session.commit()
    return item_id