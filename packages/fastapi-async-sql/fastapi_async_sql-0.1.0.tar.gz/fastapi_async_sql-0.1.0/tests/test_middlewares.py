"""Tests for the middlewares module."""

from uuid import UUID

import httpx
import pytest
from fastapi import FastAPI, Request, status
from httpx import ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_async_sql.exceptions import MissingArgsError, MultipleArgsError
from fastapi_async_sql.middlewares import AsyncSQLAlchemyMiddleware

from tests.models.hero_model import Hero
from tests.models.item_model import Item
from tests.models.team_model import Team
from tests.schemas.hero_schema import IHeroRead


@pytest.fixture(scope="function")
def app():
    """Create a FastAPI app."""
    return FastAPI()


@pytest.fixture(scope="function")
def app_with_db_middleware(app, engine: AsyncEngine):
    """Create a FastAPI app with the AsyncSQLAlchemyMiddleware."""
    app.add_middleware(AsyncSQLAlchemyMiddleware, custom_engine=engine)  # noqa
    return app


@pytest.fixture(scope="function")
async def client(app: FastAPI, test_server_url: str) -> httpx.AsyncClient:
    """Create the test client."""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url=test_server_url
    ) as client:
        yield client


async def test_init_async_sqlalchemy_middleware(app: FastAPI, database_url: str):
    """Test that the middleware is correctly initialised."""
    mw = AsyncSQLAlchemyMiddleware(app, db_url=database_url)
    assert isinstance(mw, BaseHTTPMiddleware)


async def test_init_async_sqlalchemy_middleware_custom_engine(
    app: FastAPI, engine: AsyncEngine
):
    """Test that the middleware is correctly initialised with a custom engine."""
    mw = AsyncSQLAlchemyMiddleware(app, custom_engine=engine)
    assert isinstance(mw, BaseHTTPMiddleware)


async def test_init_async_sqlalchemy_middleware_missing_required_args(app: FastAPI):
    """Test that the middleware raises an error if no db_url or custom_engine is passed."""
    with pytest.raises(MissingArgsError) as exc:
        AsyncSQLAlchemyMiddleware(app)
    assert str(exc.value) == "You need to pass db_url or custom_engine parameter."


async def test_init_async_sqlalchemy_middleware_multiple_args(
    app: FastAPI, database_url: str, engine: AsyncEngine
):
    """Test that the middleware raises an error if both db_url and custom_engine are passed."""
    with pytest.raises(MultipleArgsError) as exc:
        AsyncSQLAlchemyMiddleware(app, db_url=database_url, custom_engine=engine)
    assert str(exc.value) == "Mutually exclusive parameters: db_url, custom_engine."


async def test_init_async_sqlalchemy_middleware_correct_optional_args(
    app: FastAPI, database_url: str
):
    """Test that the middleware is correctly initialised with optional arguments."""
    engine_options = {"echo": True, "poolclass": NullPool}
    session_options = {"autoflush": False}

    mw = AsyncSQLAlchemyMiddleware(
        app,
        database_url,
        engine_options=engine_options,
        session_options=session_options,
    )

    assert mw.engine.echo

    async with mw.async_session() as session:
        assert session.bind.echo is True
        assert session.bind.pool.__class__ == NullPool
        assert session.autoflush is False


async def test_init_async_sqlalchemy_middleware_incorrect_optional_args(
    app: FastAPI,
):
    """Test that the middleware is correctly initialised with incorrect optional arguments."""
    with pytest.raises(TypeError) as exc:
        AsyncSQLAlchemyMiddleware(
            app, db_url="sqlite+aiosqlite://", invalid_args="test"
        )
    assert (
        str(exc.value)
        == "AsyncSQLAlchemyMiddleware.__init__() got an unexpected keyword argument 'invalid_args'"
    )


async def test_async_sqlalchemy_middleware_inside_route(
    app_with_db_middleware: FastAPI, client: httpx.AsyncClient
):
    """Test that the middleware correctly initialises the session within a route."""

    @app_with_db_middleware.get("/test")
    async def get_test(request: Request):
        assert isinstance(request.state.db, AsyncSession)

    response = await client.get("/test")
    assert response.status_code == 200


async def test_async_sqlalchemy_middleware_inside_route_without_middleware_fails(
    app: FastAPI, client: httpx.AsyncClient
):
    """Test that trying to access the session without the middleware raises an error."""

    @app.get("/test")
    async def get_test(request: Request):
        """Test route."""
        with pytest.raises(AttributeError):
            request.state.db  # noqa

    await client.get("/test")


async def test_async_sqlalchemy_middleware_db_session_commit(
    app_with_db_middleware: FastAPI,
    client: httpx.AsyncClient,
    db: AsyncSession,
    team: Team,
    item: Item,
):
    """Test that the middleware correctly commits the session."""

    @app_with_db_middleware.post(
        "/heroes", response_model=IHeroRead, status_code=status.HTTP_201_CREATED
    )
    async def create_hero(request: Request):
        hero = Hero(
            name="Batman",
            secret_identity="Bruce Wayne",  # nosec: B106
            age=40,
            team_id=team.id,
            item_id=item.id,
        )
        request.state.db.add(hero)
        await request.state.db.commit()
        await request.state.db.refresh(hero)
        return hero

    response = await client.post("/heroes")
    assert response.status_code == status.HTTP_201_CREATED
    hero_id = response.json()["id"]

    assert_hero = await db.get(Hero, UUID(hero_id))
    assert assert_hero.name == "Batman"
    assert assert_hero.secret_identity == "Bruce Wayne"  # nosec: B105
    assert assert_hero.age == 40
