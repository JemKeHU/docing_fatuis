from pydantic import BaseModel, Field, ConfigDict

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Item name")

class ItemCreate(ItemBase):
    pass

class ItemPut(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Item name")
    is_done: bool 

class ItemPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100, description="Item name")
    is_done: bool | None = None

class ItemRead(ItemBase):
    id: int
    is_done: bool
    model_config = ConfigDict(from_attributes=True)