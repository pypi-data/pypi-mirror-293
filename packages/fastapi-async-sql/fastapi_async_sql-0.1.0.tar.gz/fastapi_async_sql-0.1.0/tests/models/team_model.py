"""Team model for testing."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from fastapi_async_sql.models import BaseSQLModel, BaseTimestampModel, BaseUUIDModel

if TYPE_CHECKING:
    from .hero_model import Hero


class TeamBase(BaseSQLModel):
    name: str = Field(unique=True)
    headquarters: str


class Team(BaseUUIDModel, TeamBase, BaseTimestampModel, table=True):
    heroes: list["Hero"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
