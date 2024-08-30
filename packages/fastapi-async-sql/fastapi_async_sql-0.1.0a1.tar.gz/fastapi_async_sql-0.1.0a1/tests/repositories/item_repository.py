"""Repository for Item model."""

from fastapi_async_sql.repositories import BaseRepository

from ..models.item_model import Item
from ..schemas.item_schema import IItemCreate, IItemUpdate


class ItemRepository(BaseRepository[Item, IItemCreate, IItemUpdate]):
    pass
