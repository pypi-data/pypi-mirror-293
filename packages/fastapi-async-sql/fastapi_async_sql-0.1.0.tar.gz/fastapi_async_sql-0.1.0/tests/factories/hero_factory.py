"""Factory for creating Hero instances for testing."""

import factory
from factory import Faker

from ..models.hero_model import Hero
from ._base import AsyncSQLModelFactory
from .item_factory import ItemFactory
from .team_factory import TeamFactory


class HeroFactory(AsyncSQLModelFactory):
    class Meta:
        model = Hero

    name = factory.Sequence(lambda n: f"Hero {n}")
    secret_identity = Faker("name")
    age = Faker("random_int", min=1, max=100)
    team = factory.SubFactory(TeamFactory)
    item = factory.SubFactory(ItemFactory)
