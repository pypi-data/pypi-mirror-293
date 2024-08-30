"""Hero model."""

from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlmodel import Field, Relationship

from fastapi_async_sql.models import BaseSQLModel, BaseTimestampModel, BaseUUIDModel

if TYPE_CHECKING:
    from .item_model import Item
    from .team_model import Team


class HeroBase(BaseSQLModel):
    name: str = Field(unique=True)
    secret_identity: str | None = None
    age: int
    team_id: UUID4 = Field(foreign_key="teams.id")
    item_id: UUID4 = Field(foreign_key="items.id")


class Hero(BaseUUIDModel, HeroBase, BaseTimestampModel, table=True):
    team: "Team" = Relationship(back_populates="heroes")
    item: "Item" = Relationship(back_populates="heroes")
