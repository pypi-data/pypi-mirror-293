"""Factory for creating Team instances for testing."""

import factory

from ..models.team_model import Team
from ._base import AsyncSQLModelFactory


class TeamFactory(AsyncSQLModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f"Team {n}")
    headquarters = factory.Faker("city")
