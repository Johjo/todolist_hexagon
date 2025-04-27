from uuid import uuid4

import pytest
from datetime_provider import DateTimeProviderDeterministic

from test_todolist.fixture import NOW
from todolist_hexagon.events import TaskClosed
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCase


@pytest.fixture
def event_store() -> EventStoreInMemory:
    return EventStoreInMemory()

@pytest.fixture
def sut(event_store: EventStoreInMemory, datetime_provider: DateTimeProviderDeterministic) -> TodolistUseCase:
    return TodolistUseCase(event_store=event_store, datetime_provider=datetime_provider)


def test_task_closed_when_close_task(sut: TodolistUseCase, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    sut.close_task(task_key=task_key)

    assert TaskClosed(when=NOW) in event_store.events_for(key=task_key)
