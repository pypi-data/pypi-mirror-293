"""Configuration for the tests."""

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_async_sql.middlewares import AsyncSQLAlchemyMiddleware
from fastapi_async_sql.models import BaseSQLModel

from tests.factories import HeroFactory, ItemFactory, TeamFactory, register_factories
from tests.models.hero_model import Hero
from tests.models.item_model import Item
from tests.models.team_model import Team
from tests.repositories import HeroRepository, ItemRepository

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def database_url() -> str:
    """Get the database url."""
    return DATABASE_URL


@pytest.fixture(scope="session")
def test_server_url() -> str:
    """Get the test server URL."""
    return "http://testserver"


@pytest.fixture(scope="session")
def engine(database_url: str) -> AsyncEngine:
    """Get the database engine."""
    return create_async_engine(database_url)


@pytest.fixture(autouse=True)
async def create_tables(engine: AsyncEngine):
    """Create the database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQLModel.metadata.drop_all)
        await conn.run_sync(BaseSQLModel.metadata.create_all)

    yield  # Run the tests.

    async with engine.begin() as conn:
        await conn.run_sync(BaseSQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def db(engine: AsyncEngine) -> AsyncSession:
    """Get the database session."""
    async_session = async_sessionmaker(engine, class_=AsyncSession)
    async with async_session() as _session:
        register_factories(_session)
        yield _session


@pytest.fixture(scope="function")
def app(engine: AsyncEngine) -> FastAPI:
    """Create the FastAPI app."""
    app = FastAPI()
    app.add_middleware(
        AsyncSQLAlchemyMiddleware,  # noqa
        custom_engine=engine,
    )
    return app


@pytest.fixture(scope="function")
async def client(app: FastAPI, test_server_url: str) -> httpx.AsyncClient:
    """Create the test client."""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url=test_server_url
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def hero_repository(db: AsyncSession) -> HeroRepository:
    """Create a hero repository."""
    return HeroRepository(Hero, db)


@pytest.fixture(scope="function")
async def item_repository(db: AsyncSession) -> ItemRepository:
    """Create an item repository."""
    return ItemRepository(Item, db)


@pytest.fixture
async def team(db: AsyncSession) -> Team:
    """Create a team."""
    _team = TeamFactory()
    await db.flush()
    return _team


@pytest.fixture
async def item(db: AsyncSession) -> Item:
    """Create an item."""
    _item = ItemFactory()
    await db.flush()
    return _item


@pytest.fixture
async def hero(db: AsyncSession) -> Hero:
    """Create a hero."""
    _hero = HeroFactory()
    await db.flush()
    return _hero


@pytest.fixture
async def heroes(db: AsyncSession) -> list[Hero]:
    """Create heroes."""
    _heroes = HeroFactory.create_batch(100)
    await db.flush()
    return _heroes


@pytest.fixture
async def marvel_heroes(db: AsyncSession) -> list[Hero]:
    """Create 10 Marvel heroes for a test."""
    team_avengers = TeamFactory(name="Avengers", headquarters="New York")
    team_guardians = TeamFactory(
        name="Guardians of the Galaxy", headquarters="Knowhere"
    )
    heroes = [
        HeroFactory(
            name="Captain America",
            age=40,
            secret_identity="Steve Rogers",
            team=team_avengers,
        ),  # nosec:B106
        HeroFactory(
            name="Iron Man", age=45, secret_identity="Tony Stark", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Thor", age=50, secret_identity="Thor Odinson", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Hulk", age=55, secret_identity="Bruce Banner", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Spiderman", age=17, secret_identity="Peter Parker", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Black Widow",
            age=33,
            secret_identity="Natasha Romanoff",
            team=team_avengers,
        ),  # nosec:B106
        HeroFactory(
            name="Black Panther", age=34, secret_identity="T'Challa", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Hawkeye", age=43, secret_identity="Clint Barton", team=team_avengers
        ),  # nosec:B106
        HeroFactory(
            name="Captain Marvel",
            age=30,
            secret_identity="Carol Danvers",
            team=team_avengers,
        ),  # nosec:B106
        HeroFactory(name="Vision", age=35, secret_identity=None, team=team_avengers),
        HeroFactory(
            name="Star-Lord", age=35, secret_identity="Peter Quill", team=team_guardians
        ),  # nosec:B106
        HeroFactory(name="Gamora", age=35, secret_identity=None, team=team_guardians),
        HeroFactory(name="Drax", age=35, secret_identity=None, team=team_guardians),
        HeroFactory(name="Rocket", age=35, secret_identity=None, team=team_guardians),
        HeroFactory(name="Groot", age=35, secret_identity=None, team=team_guardians),
    ]
    await db.flush()
    return heroes
