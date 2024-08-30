"""Tests for core functionalities."""

from urllib.parse import urlencode

import httpx
import pytest
from fastapi import Depends, FastAPI, status
from fastapi_filter import with_prefix
from pydantic import UUID4, ConfigDict, Field
from sqlalchemy.orm import selectinload
from sqlmodel import select

from fastapi_async_sql.filtering import Filter, FilterDepends
from fastapi_async_sql.pagination import Page, Params
from fastapi_async_sql.utils.string import to_camel

from tests.dependencies import AnnotatedRepositoryHero
from tests.models.hero_model import Hero
from tests.models.team_model import Team
from tests.schemas.hero_schema import IHeroRead, IHeroReadWithTeam


@pytest.mark.parametrize(
    "query_params,slice_,expected_pages",
    [
        ({"size": 10, "page": 1}, slice(0, 10), 10),
        ({"size": 10, "page": 2}, slice(10, 20), 10),
        ({"size": 100, "page": 1}, slice(0, 100), 1),
        ({"size": 10, "page": 11}, slice(100, 110), 10),
        ({"size": 10, "page": 12}, slice(110, 120), 10),
    ],
    ids=["first_page", "second_page", "single_page", "last_page", "empty_page"],
)
async def test_get_paginated_response(
    app: FastAPI,
    client: httpx.AsyncClient,
    heroes: list[Hero],
    query_params: dict,
    slice_: slice,
    expected_pages: int,
):
    """Test get paginated response."""

    @app.get("/heroes")
    async def get_heroes(
        repository: AnnotatedRepositoryHero, params: Params = Depends()
    ) -> Page[IHeroRead]:
        return await repository.get_multi_paginated(page_params=params)

    response = await client.get("/heroes", params=query_params)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == {
        "items": [
            {
                "id": str(hero.id),
                "name": hero.name,
                "secretIdentity": hero.secret_identity,
                "age": hero.age,
                "teamId": str(hero.team_id),
                "itemId": str(hero.item_id),
            }
            for hero in heroes[slice_]
        ],
        "total": len(heroes),
        "page": query_params["page"],
        "pages": expected_pages,
        "size": query_params["size"],
    }


@pytest.mark.parametrize(
    "filter_clause,endpoint,expected",
    [
        ({"name": "Captain America"}, "/heroes", ["Captain America"]),
        (
            {"name__neq": "Captain America"},
            "/heroes",
            [
                "Iron Man",
                "Thor",
                "Hulk",
                "Spiderman",
                "Black Widow",
                "Black Panther",
                "Hawkeye",
                "Captain Marvel",
                "Vision",
                "Star-Lord",
                "Gamora",
                "Drax",
                "Rocket",
                "Groot",
            ],
        ),
        ({"age__gt": 40}, "/heroes", ["Iron Man", "Thor", "Hulk", "Hawkeye"]),
        ({"age__gte": 50}, "/heroes", ["Thor", "Hulk"]),
        ({"age__lt": 20}, "/heroes", ["Spiderman"]),
        ({"age__lte": 30}, "/heroes", ["Spiderman", "Captain Marvel"]),
        ({"name__like": "Captain%"}, "/heroes", ["Captain America", "Captain Marvel"]),
        ({"name__ilike": "%man"}, "/heroes", ["Iron Man", "Spiderman"]),
        (
            {"name__in": "Captain America,Iron Man"},
            "/heroes",
            ["Captain America", "Iron Man"],
        ),
        ([("name__in", "Iron Man")], "/heroes", ["Iron Man"]),
        (
            {"name__not_in": "Vision,Captain America,Iron Man"},
            "/heroes",
            [
                "Thor",
                "Hulk",
                "Spiderman",
                "Black Widow",
                "Black Panther",
                "Hawkeye",
                "Captain Marvel",
                "Star-Lord",
                "Gamora",
                "Drax",
                "Rocket",
                "Groot",
            ],
        ),
        (
            {"secret_identity__isnull": True},
            "/heroes",
            ["Vision", "Gamora", "Drax", "Rocket", "Groot"],
        ),
        (
            {"secret_identity__isnull": False},
            "/heroes",
            [
                "Captain America",
                "Iron Man",
                "Thor",
                "Hulk",
                "Spiderman",
                "Black Widow",
                "Black Panther",
                "Hawkeye",
                "Captain Marvel",
                "Star-Lord",
            ],
        ),
        (
            {"secretIdentityIsnull": True},
            "/heroes-by-alias",
            ["Vision", "Gamora", "Drax", "Rocket", "Groot"],
        ),
        (
            {"secretIdentityIsnull": False},
            "/heroes-by-alias",
            [
                "Captain America",
                "Iron Man",
                "Thor",
                "Hulk",
                "Spiderman",
                "Black Widow",
                "Black Panther",
                "Hawkeye",
                "Captain Marvel",
                "Star-Lord",
            ],
        ),
        ({"name__like": "Black%", "age__gt": 33}, "/heroes", ["Black Panther"]),
        ({"age__gt": 40, "age__lt": 55}, "/heroes", ["Iron Man", "Thor", "Hawkeye"]),
        (
            {"team__headquarters": "New York"},
            "/heroes",
            [
                "Captain America",
                "Iron Man",
                "Thor",
                "Hulk",
                "Spiderman",
                "Black Widow",
                "Black Panther",
                "Hawkeye",
                "Captain Marvel",
                "Vision",
            ],
        ),
        (
            {"order_by": "name"},
            "/heroes",
            [
                "Black Panther",
                "Black Widow",
                "Captain America",
                "Captain Marvel",
                "Drax",
                "Gamora",
                "Groot",
                "Hawkeye",
                "Hulk",
                "Iron Man",
                "Rocket",
                "Spiderman",
                "Star-Lord",
                "Thor",
                "Vision",
            ],
        ),
        (
            {"order_by": "-name"},
            "/heroes",
            [
                "Vision",
                "Thor",
                "Star-Lord",
                "Spiderman",
                "Rocket",
                "Iron Man",
                "Hulk",
                "Hawkeye",
                "Groot",
                "Gamora",
                "Drax",
                "Captain Marvel",
                "Captain America",
                "Black Widow",
                "Black Panther",
            ],
        ),
        ({"search": "Captain"}, "/heroes", ["Captain America", "Captain Marvel"]),
        ({"search": "Steve Rogers"}, "/heroes", ["Captain America"]),
    ],
    ids=[
        "name",
        "name__neq",
        "age__gt",
        "age__gte",
        "age__lt",
        "age__lte",
        "name__like",
        "name__ilike",
        "name__in",
        "name__in_single_query_param",
        "name__not_in",
        "secret_identity__isnull",
        "secret_identity__isnull_false",
        "secretIdentityIsnull",
        "secretIdentityIsnull_false",
        "name__like_and_age__gt",
        "age__gt_and_age__lt",
        "team__headquarters",
        "order_by_name",
        "order_by_name_desc",
        "search_by_name",
        "search_by_secret_identity",
    ],
)
async def test_api_filtering(
    app: FastAPI,
    client: httpx.AsyncClient,
    marvel_heroes,
    filter_clause: dict,
    endpoint: str,
    expected,
) -> None:
    """Test API filtering."""

    class TeamFilter(Filter):
        name: str | None = None
        headquarters: str | None = None
        order_by: list[str] | None = Field(default_factory=list)

        class Constants(Filter.Constants):
            model = Team

    class HeroFilter(Filter):
        name: str | None = None
        name__neq: str | None = None
        name__like: str | None = None
        name__ilike: str | None = None
        name__in: list[str] | None = Field(default_factory=list)
        name__not_in: list[str] | None = None
        age__gt: str | None = None
        age__gte: str | None = None
        age__lt: str | None = None
        age__lte: str | None = None
        age: int | None = None
        secret_identity: str | None = None
        secret_identity__isnull: bool | None = None
        order_by: list[str] | None = Field(default_factory=list)
        team: TeamFilter | None = FilterDepends(with_prefix("team", TeamFilter))
        search: str | None = None

        class Constants(Filter.Constants):
            model = Hero
            search_model_fields = ["name", "secret_identity"]

    class HeroFilterByAlias(HeroFilter):
        model_config = ConfigDict(
            alias_generator=to_camel,
            populate_by_name=True,
        )

    @app.get("/heroes")
    async def get_heroes(
        repository: AnnotatedRepositoryHero,
        params: Params = Depends(),
        filter_by: HeroFilter = FilterDepends(HeroFilter),
    ) -> list[IHeroRead]:
        query = select(Hero).outerjoin(Team)
        return await repository.get_multi(
            query=query, page_params=params, filter_by=filter_by
        )

    @app.get("/heroes-by-alias")
    async def get_heroes_by_alias(
        repository: AnnotatedRepositoryHero,
        params: Params = Depends(),
        filter_by: HeroFilterByAlias = FilterDepends(HeroFilterByAlias, by_alias=True),
    ) -> list[IHeroRead]:
        return await repository.get_multi(page_params=params, filter_by=filter_by)

    response = await client.get(f"{endpoint}?{urlencode(filter_clause)}")
    assert response.status_code == status.HTTP_200_OK, response.json()
    response_data = response.json()
    response_names = [hero["name"] for hero in response_data]
    assert response_names == expected


async def test_get_heroes_with_relationships(
    app: FastAPI, client: httpx.AsyncClient, heroes: list[Hero]
):
    """Test get heroes with relationship."""

    @app.get("/heroes")
    async def get_heroes(
        repository: AnnotatedRepositoryHero,
    ) -> list[IHeroReadWithTeam]:
        query = (
            select(Hero)
            .options(selectinload(Hero.team))
            .options(selectinload(Hero.item))
        )
        response = await repository.get_multi(query=query)
        return response

    response = await client.get("/heroes")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert response_data == [
        {
            "id": str(hero.id),
            "name": hero.name,
            "secretIdentity": hero.secret_identity,
            "age": hero.age,
            "teamId": str(hero.team_id),
            "team": {
                "id": str(hero.team.id),
                "name": hero.team.name,
                "headquarters": hero.team.headquarters,
            },
            "itemId": str(hero.item_id),
            "item": {
                "id": str(hero.item.id),
                "name": hero.item.name,
                "createdById": str(hero.item.created_by_id),
            },
        }
        for hero in heroes
    ]


async def test_get_hero_with_relationships_with_lazy_loading(
    app: FastAPI, client: httpx.AsyncClient, hero: Hero
):
    """Test get heroes with relationship with lazy loading."""

    @app.get("/heroes/{hero_id}")
    async def get_heroes(
        hero_id: UUID4, repository: AnnotatedRepositoryHero
    ) -> IHeroReadWithTeam:
        response = await repository.get(id=hero_id)
        response.item = await response.awaitable_attrs.item
        response.team = await response.awaitable_attrs.team

        return response

    response = await client.get(f"/heroes/{hero.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert response_data == {
        "id": str(hero.id),
        "name": hero.name,
        "secretIdentity": hero.secret_identity,
        "age": hero.age,
        "teamId": str(hero.team_id),
        "team": {
            "id": str(hero.team.id),
            "name": hero.team.name,
            "headquarters": hero.team.headquarters,
        },
        "itemId": str(hero.item_id),
        "item": {
            "id": str(hero.item.id),
            "name": hero.item.name,
            "createdById": str(hero.item.created_by_id),
        },
    }
