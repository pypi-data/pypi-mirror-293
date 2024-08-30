"""Factory for creating Item instances for testing."""

import factory

from ..models.item_model import Item
from ._base import AsyncSQLModelFactory


class ItemFactory(AsyncSQLModelFactory):
    class Meta:
        model = Item

    name = factory.Faker("word")
    created_by_id = factory.Faker("uuid4")
