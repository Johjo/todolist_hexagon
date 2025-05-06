from uuid import uuid4

from test_todolist.fixture import NOW
from todolist_hexagon.events import TaskOpened, TaskDescribed, SubTaskAttached
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort


def test_task_opened_when_open_sub_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    parent_task_key = uuid4()
    children_task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_sub_task(parent_task_key=parent_task_key, children_task_key=children_task_key, title=task_title,
                      description=task_description)
    assert TaskOpened(when=NOW) in event_store.events_for(key=children_task_key)


def test_task_described_when_open_sub_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    parent_task_key = uuid4()
    children_task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_sub_task(parent_task_key=parent_task_key, children_task_key=children_task_key, title=task_title,
                      description=task_description)
    assert TaskDescribed(title=task_title, description=task_description, when=NOW) in event_store.events_for(
        key=children_task_key)


def test_task_attached_to_parent_task_when_open_sub_task(sut: TodolistUseCasePort,
                                                         event_store: EventStoreInMemory) -> None:
    parent_task_key = uuid4()
    children_task_key = uuid4()
    task_title = f"some title{uuid4()}"
    task_description = f"some description{uuid4()}"
    sut.open_sub_task(parent_task_key=parent_task_key, children_task_key=children_task_key, title=task_title,
                      description=task_description)

    assert SubTaskAttached(task_key=children_task_key, when=NOW) in event_store.events_for(key=parent_task_key)
