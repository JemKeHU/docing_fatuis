from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from database import Model

class ItemModel(Model):
    __tablename__ = "items"

    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    is_done: Mapped[bool] = mapped_column(default=False, nullable=False) 