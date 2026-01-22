from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(min_length=2, max_length=100, description="Item name")

class ItemCreate(ItemBase):
    id: int = Field(...)
    is_done: bool = Field(default=False)