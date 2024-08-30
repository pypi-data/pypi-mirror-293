"""Base model."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import AwareDatetime, ConfigDict
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import TIMESTAMP, Field, SQLModel

from fastapi_async_sql.utils.string import to_camel, to_snake_plural


class BaseSQLModel(AsyncAttrs, SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically."""
        return to_snake_plural(cls.__name__)

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_assignment=True,
        populate_by_name=True,
        extra="forbid",
    )


class BaseTimestampModel:
    created_at: AwareDatetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        sa_type=TIMESTAMP(timezone=True),
    )

    updated_at: AwareDatetime | None = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.now(tz=timezone.utc)},
    )


class BaseUUIDModel:
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
