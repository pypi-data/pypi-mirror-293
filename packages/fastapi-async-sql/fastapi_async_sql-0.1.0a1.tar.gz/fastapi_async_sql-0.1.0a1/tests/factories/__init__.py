"""Factories module for tests."""

import sys

from factory.alchemy import SQLAlchemyModelFactory
from sqlmodel.ext.asyncio.session import AsyncSession

from .hero_factory import HeroFactory  # noqa: F401
from .item_factory import ItemFactory  # noqa: F401
from .team_factory import TeamFactory  # noqa: F401


def register_factories(session: AsyncSession) -> None:
    """Register all factories in the session.

    Args:
        session: An instance of the AsyncSession.

    Returns: None
    """
    import inspect

    for _class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(_class[1], SQLAlchemyModelFactory):
            _class[1]._meta.sqlalchemy_session = session
