from uuid import uuid4

from test_todolist.fixture import NOW, PREVIOUSLY
from todolist_hexagon.base.ports import AggregateEvent
from todolist_hexagon.events import TaskClosed, TaskDescribed
from todolist_hexagon.result import Ok, Err
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort, TaskNotFound, TaskAlreadyClosed


def test_task_is_closed(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    event_store.save(AggregateEvent(key=task_key, events=[TaskDescribed(when=PREVIOUSLY)]))

    sut.close_task(task_key=task_key)

    assert TaskClosed(when=NOW) in event_store.events_for(key=task_key)


def test_tell_ok(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    event_store.save(AggregateEvent(key=task_key, events=[TaskDescribed(when=PREVIOUSLY)]))

    response = sut.close_task(task_key=task_key)

    assert response == Ok(None)


def test_tell_if_task_not_found(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()

    response = sut.close_task(task_key=task_key)

    assert response == Err(TaskNotFound())


def test_dont_close_task_already_closed(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    event_store.save(AggregateEvent(key=task_key, events=[TaskClosed(when=PREVIOUSLY)]))

    sut.close_task(task_key=task_key)

    assert not TaskClosed(when=NOW) in event_store.events_for(key=task_key)

def test_tell_if_task_already_closed(sut: TodolistUseCasePort, event_store: EventStoreInMemory) -> None:
    task_key = uuid4()
    event_store.save(AggregateEvent(key=task_key, events=[TaskClosed(when=PREVIOUSLY)]))

    response = sut.close_task(task_key=task_key)

    assert response == Err(TaskAlreadyClosed())

