from uuid import uuid4

import pytest

from test_todolist.datetime_provider_fixed import DateTimeProviderFixed
from test_todolist.fixture import NOW
from todolist_hexagon.events import TodoListCreated
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()

@pytest.fixture
def sut(event_store: EventStoreInMemory, datetime_provider: DateTimeProviderFixed) -> TodolistUseCase:
    return TodolistUseCase(event_store=event_store, datetime_provider=datetime_provider)

def test_todolist_created_when_create_todolist(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()

    sut.create_todolist(todolist_key=todolist_key)

    assert TodoListCreated(todolist_key=todolist_key, when=NOW) in event_store.events_for(key=todolist_key)


def test_todolist_created_one_time_when_create_same_todolist_twice(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()

    sut.create_todolist(todolist_key=todolist_key)
    sut.create_todolist(todolist_key=todolist_key)

    assert event_store.events_for(key=todolist_key) == [TodoListCreated(todolist_key=todolist_key, when=NOW)]


def test_two_todolist_created_when_create_two_todolist(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key_one = uuid4()
    todolist_key_two = uuid4()

    sut.create_todolist(todolist_key=todolist_key_one)
    sut.create_todolist(todolist_key=todolist_key_two)

    assert TodoListCreated(todolist_key=todolist_key_one, when=NOW) in event_store.events_for(key=todolist_key_one)
    assert TodoListCreated(todolist_key=todolist_key_two, when=NOW) in event_store.events_for(key=todolist_key_two)


