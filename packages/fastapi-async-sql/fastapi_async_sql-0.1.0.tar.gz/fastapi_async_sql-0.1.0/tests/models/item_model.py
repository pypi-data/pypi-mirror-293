"""Item model."""

from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Relationship

from fastapi_async_sql.models import BaseSQLModel, BaseTimestampModel, BaseUUIDModel

if TYPE_CHECKING:
    from .hero_model import Hero


class ItemBase(BaseSQLModel):
    name: str


class Item(BaseUUIDModel, ItemBase, BaseTimestampModel, table=True):
    created_by_id: UUID4
    heroes: list["Hero"] = Relationship(
        back_populates="item",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
