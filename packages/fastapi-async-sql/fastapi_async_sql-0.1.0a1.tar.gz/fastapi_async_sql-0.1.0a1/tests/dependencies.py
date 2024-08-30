"""Dependencies module."""

from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from .models.hero_model import Hero
from .repositories.hero_repository import HeroRepository


def get_db(request: Request) -> AsyncSession:
    """Get the database session."""
    return request.state.db


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_hero_repository(db: DbSession) -> HeroRepository:
    """Get the hero repository."""
    return HeroRepository(Hero, db=db)


AnnotatedRepositoryHero = Annotated[HeroRepository, Depends(get_hero_repository)]
