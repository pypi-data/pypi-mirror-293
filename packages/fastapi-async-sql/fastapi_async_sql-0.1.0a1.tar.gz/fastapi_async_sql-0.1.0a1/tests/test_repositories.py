"""Tests for Repository."""

from datetime import datetime
from uuid import uuid4

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_async_sql.exceptions import CreateObjectError, ObjectNotFoundError
from fastapi_async_sql.pagination import Params

from tests.models.hero_model import Hero
from tests.models.item_model import Item
from tests.models.team_model import Team
from tests.repositories import HeroRepository, ItemRepository
from tests.schemas.hero_schema import IHeroCreate, IHeroUpdate
from tests.schemas.item_schema import IItemCreate


async def test_create_hero(
    db: AsyncSession,
    team: Team,
    item: Item,
    hero_repository: HeroRepository,
):
    """Test create hero."""
    hero_data = IHeroCreate(
        name="Test Hero",
        age=30,
        secret_identity="Test Identity",  # nosec: B106
        team_id=team.id,
        item_id=item.id,
    )
    created_hero = await hero_repository.create(obj_in=hero_data)
    assert created_hero.name == "Test Hero"
    assert created_hero.age == 30
    assert created_hero.secret_identity == "Test Identity"  # nosec: B105
    assert isinstance(created_hero.created_at, datetime)
    assert created_hero.updated_at is None


async def test_create_item_with_extra_data(
    db: AsyncSession,
    item_repository: ItemRepository,
):
    """Test create item with extra data."""
    item_data = IItemCreate(name="Test Item")
    created_by_id = uuid4()
    created_item = await item_repository.create(
        obj_in=item_data, created_by_id=created_by_id
    )
    assert created_item.name == "Test Item"
    assert created_item.created_by_id == created_by_id


async def test_create_hero_duplicate(
    db: AsyncSession,
    heroes: list[Hero],
    team: Team,
    item: Item,
    hero_repository: HeroRepository,
):
    """Test create hero with duplicate data."""
    hero_data = IHeroCreate(
        name=heroes[0].name,
        age=30,
        secret_identity="Test Identity",  # nosec: B106
        team_id=team.id,
        item_id=item.id,
    )
    with pytest.raises(CreateObjectError):
        await hero_repository.create(obj_in=hero_data)


async def test_get_hero(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test get hero."""
    hero = heroes[0]
    retrieved_hero = await hero_repository.get(id=hero.id)
    assert retrieved_hero.id == hero.id
    assert retrieved_hero.name == hero.name
    assert retrieved_hero.team == hero.team


async def test_get_hero_not_found(
    db: AsyncSession,
    hero_repository: HeroRepository,
):
    """Test get hero not found."""
    with pytest.raises(ObjectNotFoundError):
        await hero_repository.get(id=uuid4())


async def test_get_multi_hero(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test get multiple heroes."""
    retrieved_heroes = await hero_repository.get_multi()
    assert len(retrieved_heroes) == len(heroes)


async def test_get_multi_paginated_hero(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test get multiple heroes paginated."""
    retrieved_heroes = await hero_repository.get_multi_paginated()
    assert len(retrieved_heroes.items) == min(
        len(heroes), Params.model_fields["size"].default
    )


async def test_update_hero(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test update hero."""
    hero = heroes[0]
    assert hero.updated_at is None
    update_data = IHeroUpdate(name="Updated Hero")
    updated_hero = await hero_repository.update(obj_current=hero, obj_new=update_data)
    assert updated_hero.name == "Updated Hero"
    assert isinstance(updated_hero.updated_at, datetime)
    assert updated_hero.updated_at > hero.created_at


async def test_update_hero_with_dict(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test update hero with dict."""
    hero = heroes[0]
    assert hero.updated_at is None
    update_data = {"name": "Updated Hero"}
    updated_hero = await hero_repository.update(obj_current=hero, obj_new=update_data)
    assert updated_hero.name == "Updated Hero"
    assert isinstance(updated_hero.updated_at, datetime)
    assert updated_hero.updated_at > hero.created_at


async def test_remove_hero(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test remove hero."""
    hero = heroes[0]
    await hero_repository.remove(id=hero.id)
    with pytest.raises(ObjectNotFoundError):
        await hero_repository.get(id=hero.id)


async def test_remove_non_existent_hero(
    db: AsyncSession,
    hero_repository: HeroRepository,
):
    """Test remove non-existent hero."""
    with pytest.raises(ObjectNotFoundError):
        await hero_repository.remove(id=uuid4())


async def test_count_heroes(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test count heroes."""
    count = await hero_repository.get_count()
    assert count == len(heroes)


async def test_get_hero_by_ids(
    db: AsyncSession,
    heroes: list[Hero],
    hero_repository: HeroRepository,
):
    """Test get heroes by IDs."""
    hero_ids = [hero.id for hero in heroes[:2]]
    retrieved_heroes = await hero_repository.get_by_ids(list_ids=hero_ids)
    assert len(retrieved_heroes) == len(hero_ids)
    for hero in retrieved_heroes:
        assert hero.id in hero_ids


async def test_repository_not_defined_session():
    """Test repository with not defined session."""
    with pytest.raises(ValueError) as exc:
        await HeroRepository(Hero).get(id=uuid4())
    assert str(exc.value) == "Database session is not set."
