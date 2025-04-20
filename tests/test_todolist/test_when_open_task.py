from uuid import uuid4

import pytest

from todolist_hexagon.events import TaskOpened, TaskAttached, TaskDescribed
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()

@pytest.fixture
def sut(event_store: EventStoreInMemory) -> TodolistUseCase:
    return TodolistUseCase(event_store)


def test_task_opened_when_open_task(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)
    assert TaskOpened() in event_store.events_for(key=task_key)


def test_task_described_when_open_task(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)
    assert TaskDescribed(title=task_title, description=task_description) in event_store.events_for(key=task_key)


def test_task_attached_to_todolist_when_open_task(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)

    assert TaskAttached(task_key=task_key) in event_store.events_for(key=todolist_key)
