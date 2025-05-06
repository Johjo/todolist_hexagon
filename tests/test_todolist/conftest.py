import pytest
from datetime_provider import DateTimeProviderDeterministic

from test_todolist.fixture import NOW
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase, TodolistUseCasePort


@pytest.fixture
def datetime_provider() -> DateTimeProviderDeterministic:
    datetime_provider = DateTimeProviderDeterministic()
    datetime_provider.feed(NOW)
    return datetime_provider

@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()

@pytest.fixture
def sut(event_store: EventStoreInMemory, datetime_provider: DateTimeProviderDeterministic) -> TodolistUseCasePort:
    return TodolistUseCase(event_store, datetime_provider=datetime_provider)
