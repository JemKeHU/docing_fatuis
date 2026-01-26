from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Item name")

class ItemCreate(ItemBase):
    id: int
    is_done: bool = False

class ItemChange(BaseModel):
    name: str
    is_done: bool