"""Test utils functions."""

from fastapi_async_sql.models import BaseSQLModel, BaseUUIDModel
from fastapi_async_sql.utils.partial import optional


class DummySchema(BaseUUIDModel, BaseSQLModel, table=True):  # type: ignore
    name: str
    age: int


def test_optional_schema():
    """Test optional function."""
    fields_to_exclude = {"id"}
    fields_to_partial = {"name", "age"}

    @optional(without_fields=fields_to_exclude)
    class NewSchema(DummySchema): ...

    # NewSchema should not have excluded fields
    for field in fields_to_exclude:
        assert field not in NewSchema.model_fields

    # NewSchema should have non-excluded fields
    for field in fields_to_partial:
        assert field in NewSchema.model_fields
        # NewSchema should have partial fields
        assert NewSchema.model_fields[field].is_required() is False


def test_optional_schema_with_default_fields():
    """Test optional function with default fields."""

    @optional(without_fields={"id"})
    class NewSchema(DummySchema): ...

    # NewSchema should have nullable default fields
    assert NewSchema.model_fields["age"].default is None

    assert NewSchema(name="test").model_dump() == {"name": "test", "age": None}
