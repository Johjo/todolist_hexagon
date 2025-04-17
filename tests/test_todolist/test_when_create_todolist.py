from uuid import uuid4

from src.events import TodoListCreated
from src.todolist_usecase import TodolistUseCase
from tests.test_todolist.event_store_for_test import EventStoreForTest


def test_todolist_created_when_create_todolist() -> None:
    todolist_key = uuid4()
    event_store = EventStoreForTest()
    sut = TodolistUseCase(event_store)

    sut.create_todolist(key=todolist_key)

    assert event_store.all_events == [TodoListCreated(key=todolist_key)]


def test_todolist_created_one_time_when_create_same_todolist_twice() -> None:
    todolist_key = uuid4()
    event_store = EventStoreForTest()
    sut = TodolistUseCase(event_store)

    sut.create_todolist(key=todolist_key)
    sut.create_todolist(key=todolist_key)

    assert event_store.all_events == [TodoListCreated(key=todolist_key)]


def test_two_todolist_created_when_create_two_todolist() -> None:
    todolist_key_one = uuid4()
    todolist_key_two = uuid4()
    event_store = EventStoreForTest()
    sut = TodolistUseCase(event_store)

    sut.create_todolist(key=todolist_key_one)
    sut.create_todolist(key=todolist_key_two)

    assert event_store.all_events == [TodoListCreated(key=todolist_key_one), TodoListCreated(key=todolist_key_two)]


