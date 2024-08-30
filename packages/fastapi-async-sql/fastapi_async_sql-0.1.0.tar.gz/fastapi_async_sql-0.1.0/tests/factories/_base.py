"""Base factory."""

from factory.alchemy import SQLAlchemyModelFactory


class AsyncSQLModelFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
