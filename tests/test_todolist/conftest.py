import pytest
from datetime_provider import DateTimeProviderDeterministic

from test_todolist.fixture import NOW


@pytest.fixture
def datetime_provider() -> DateTimeProviderDeterministic:
    datetime_provider = DateTimeProviderDeterministic()
    datetime_provider.feed(NOW)
    return datetime_provider
