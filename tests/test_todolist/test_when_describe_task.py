from uuid import uuid4

from test_todolist.fixture import NOW, PREVIOUSLY
from todolist_hexagon.base.ports import AggregateEvent
from todolist_hexagon.events import TaskOpened, TaskAttached, TaskDescribed
from todolist_hexagon.result import Err
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort, TaskNotFound


def test_title_described_when_describe_task_with_title(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    task_title = f"some title{uuid4()}"
    event_store.save(AggregateEvent(key=task_key, events=[TaskDescribed(when=PREVIOUSLY)]))

    sut.describe_task(task_key=task_key, title=task_title)

    assert TaskDescribed(title=task_title, when=NOW) in event_store.events_for(key=task_key)


def test_description_described_when_describe_task_with_description(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    task_description = f"some description{uuid4()}"
    event_store.save(AggregateEvent(key=task_key, events=[TaskDescribed(when=PREVIOUSLY)]))

    sut.describe_task(task_key=task_key, description=task_description)

    assert TaskDescribed(description=task_description, when=NOW) in event_store.events_for(key=task_key)


def test_tell_ok_when_describe_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    task_description = f"some description{uuid4()}"
    event_store.save(AggregateEvent(key=task_key, events=[TaskDescribed(when=PREVIOUSLY)]))

    response = sut.describe_task(task_key=task_key, description=task_description)

    assert response.is_ok()


def test_tell_task_not_found_when_describe_task(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    task_description = f"some description{uuid4()}"
    response = sut.describe_task(task_key=task_key, description=task_description)
    assert response == Err(TaskNotFound())




