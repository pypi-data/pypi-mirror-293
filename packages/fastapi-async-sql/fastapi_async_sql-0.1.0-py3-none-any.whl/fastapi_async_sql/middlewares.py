"""Middlewares module."""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from fastapi_async_sql.exceptions import (
    MissingArgsError,
    MultipleArgsError,
)


class AsyncSQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        db_url: str | None = None,
        custom_engine: AsyncEngine | None = None,
        session_options: dict | None = None,
        engine_options: dict | None = None,
    ):
        super().__init__(app)

        if not db_url and not custom_engine:
            raise MissingArgsError("db_url", "custom_engine")
        if db_url and custom_engine:
            raise MultipleArgsError("db_url", "custom_engine")

        if not custom_engine:
            self.engine = create_async_engine(db_url, **engine_options or {})
        else:
            self.engine = custom_engine

        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            **session_options or {},
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """Method to dispatch the request."""
        async with self.async_session() as session:
            request.state.db = session
            response = await call_next(request)
            return response
