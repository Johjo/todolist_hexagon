from uuid import uuid4

from test_todolist.fixture import NOW
from todolist_hexagon.events import TaskClosed
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort


def test_task_closed_when_close_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    sut.close_task(task_key=task_key)

    assert TaskClosed(when=NOW) in event_store.events_for(key=task_key)
