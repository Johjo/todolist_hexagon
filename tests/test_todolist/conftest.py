import pytest

from test_todolist.datetime_provider_fixed import DateTimeProviderFixed
from test_todolist.fixture import NOW


@pytest.fixture
def datetime_provider() -> DateTimeProviderFixed:
    datetime_provider = DateTimeProviderFixed()
    datetime_provider.feed(NOW)
    return datetime_provider
