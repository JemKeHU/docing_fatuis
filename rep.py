from sqlalchemy import select, delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from models.items import ItemModel
from schemas.items import ItemBase, ItemPut, ItemPatch
from typing import cast, Sequence

class ItemRepository:
    @classmethod
    async def add_item(cls, data: ItemBase, session: AsyncSession) -> ItemModel:
        task_dict = data.model_dump()
        task = ItemModel(**task_dict)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    
    @classmethod
    async def get_all_items(cls, session: AsyncSession) -> Sequence[ItemModel]:
        query = select(ItemModel)
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, item_id: int, session: AsyncSession) -> ItemModel | None:
        query = select(ItemModel).where(ItemModel.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def put_item(cls, item: ItemModel, put_item: ItemPut, session: AsyncSession) -> ItemModel:
        item.name = put_item.name
        item.is_done = put_item.is_done
        await session.commit()
        await session.refresh(item)
        return item
    
    @classmethod
    async def patch_item(cls, item: ItemModel, patch_item: ItemPatch, session: AsyncSession) -> ItemModel:
        if patch_item.name is not None:
            item.name = patch_item.name
        if patch_item.is_done is not None:
            item.is_done = patch_item.is_done
        await session.commit()
        await session.refresh(item)
        return item
    
    @classmethod
    async def delete_item(cls, item_id: int, session: AsyncSession) -> bool:
        query = delete(ItemModel).where(ItemModel.id == item_id)
        result = await session.execute(query)
        result = cast(CursorResult, result)
        await session.commit()
        return result.rowcount > 0
