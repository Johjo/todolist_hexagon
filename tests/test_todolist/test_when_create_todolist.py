from uuid import uuid4

import pytest

from todolist_hexagon.events import TodoListCreated
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()

@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistUseCase:
    return TodolistUseCase(event_store)

def test_todolist_created_when_create_todolist(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()

    sut.create_todolist(todolist_key=todolist_key)

    assert TodoListCreated(todolist_key=todolist_key) in event_store.events_for(key=todolist_key)


def test_todolist_created_one_time_when_create_same_todolist_twice(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()

    sut.create_todolist(todolist_key=todolist_key)
    sut.create_todolist(todolist_key=todolist_key)

    assert event_store.events_for(key=todolist_key) == [TodoListCreated(todolist_key=todolist_key)]


def test_two_todolist_created_when_create_two_todolist(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key_one = uuid4()
    todolist_key_two = uuid4()

    sut.create_todolist(todolist_key=todolist_key_one)
    sut.create_todolist(todolist_key=todolist_key_two)

    assert TodoListCreated(todolist_key=todolist_key_one) in event_store.events_for(key=todolist_key_one)
    assert TodoListCreated(todolist_key=todolist_key_two) in event_store.events_for(key=todolist_key_two)


