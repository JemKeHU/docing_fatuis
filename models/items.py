from sqlalchemy.orm import Mapped, mapped_column
from database import Model

class ItemModel(Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_done: Mapped[bool] 