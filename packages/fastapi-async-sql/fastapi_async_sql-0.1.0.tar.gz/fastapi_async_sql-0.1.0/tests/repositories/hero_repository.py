"""Repository for Hero model."""

from fastapi_async_sql.repositories import BaseRepository

from ..models.hero_model import Hero
from ..schemas.hero_schema import IHeroCreate, IHeroUpdate


class HeroRepository(BaseRepository[Hero, IHeroCreate, IHeroUpdate]):
    pass
