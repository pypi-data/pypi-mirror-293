"""Schemas for Item model."""

from pydantic import UUID4

from fastapi_async_sql.utils.partial import optional

from ..models.item_model import ItemBase


class IItemCreate(ItemBase): ...


@optional()
class IItemUpdate(ItemBase): ...


class IItemRead(ItemBase):
    id: UUID4
    created_by_id: UUID4
