from uuid import uuid4

from test_todolist.fixture import NOW
from todolist_hexagon.events import TaskOpened, TaskAttached, TaskDescribed
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort


def test_task_opened_when_open_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)
    assert TaskOpened(when=NOW) in event_store.events_for(key=task_key)


def test_task_described_when_open_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)
    assert TaskDescribed(title=task_title, description=task_description, when=NOW) in event_store.events_for(
        key=task_key)


def test_task_attached_to_todolist_when_open_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    todolist_key = uuid4()
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_task(todolist_key=todolist_key, task_key=task_key, title=task_title, description=task_description)

    assert TaskAttached(task_key=task_key, when=NOW) in event_store.events_for(key=todolist_key)
