"""Schemas for Hero model."""

from pydantic import UUID4

from fastapi_async_sql.utils.partial import optional

from ..models.hero_model import HeroBase
from ..models.item_model import ItemBase
from ..models.team_model import TeamBase


class IHeroCreate(HeroBase):
    pass


@optional()
class IHeroUpdate(HeroBase):
    team_id: UUID4 | None = None
    item_id: UUID4 | None = None


class IHeroRead(HeroBase):
    id: UUID4


class HeroTeamRead(TeamBase):
    id: UUID4


class ItemTeamRead(ItemBase):
    id: UUID4
    created_by_id: UUID4


class IHeroReadWithTeam(IHeroRead):
    id: UUID4
    team: HeroTeamRead = None
    item: ItemTeamRead = None
