from uuid import uuid4

import pytest

from test_todolist.fixture import NOW, PREVIOUSLY
from todolist_hexagon.base.ports import AggregateEvent
from todolist_hexagon.events import TaskClosed, TaskDescribed, TaskOpened, SubTaskAttached, TaskEvent, Event
from todolist_hexagon.result import Ok, Err
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory
from todolist_hexagon.todolist_usecase import TodolistUseCasePort
from todolist_hexagon.task_error import TaskNotFound, TaskAlreadyClosed, TaskHavingOpenedSubTask


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

    response = sut.close_task(task_key=task_key)

    assert not TaskClosed(when=NOW) in event_store.events_for(key=task_key)
    assert response == Err(TaskAlreadyClosed())


TASK_KEY_PARENT = uuid4()
TASK_KEY_CHILD_ONE = uuid4()
TASK_KEY_CHILD_TWO = uuid4()


@pytest.mark.parametrize("title, aggregate_events",
                         [["with one open task",
                           [AggregateEvent(key=TASK_KEY_PARENT, events=[TaskOpened(when=PREVIOUSLY),
                                                                        SubTaskAttached(task_key=TASK_KEY_CHILD_ONE,
                                                                                        when=PREVIOUSLY)]),
                            AggregateEvent(key=TASK_KEY_CHILD_ONE, events=[
                                TaskOpened(when=PREVIOUSLY)])]],
                          ["with one closed task and one opened",
                           [AggregateEvent(key=TASK_KEY_PARENT, events=[TaskOpened(when=PREVIOUSLY),
                                                                        SubTaskAttached(task_key=TASK_KEY_CHILD_ONE,
                                                                                        when=PREVIOUSLY),
                                                                        SubTaskAttached(task_key=TASK_KEY_CHILD_TWO,
                                                                                        when=PREVIOUSLY)]),
                            AggregateEvent(key=TASK_KEY_CHILD_ONE, events=[
                                TaskOpened(when=PREVIOUSLY), TaskClosed(when=PREVIOUSLY)]),
                            AggregateEvent(key=TASK_KEY_CHILD_TWO, events=[
                                TaskOpened(when=PREVIOUSLY)])]]])
def test_dont_close_task_having_opened_sub_task(title: str, aggregate_events: list[AggregateEvent[Event]], sut: TodolistUseCasePort,
                                                event_store: EventStoreInMemory) -> None:
    event_store.save(*aggregate_events)

    response = sut.close_task(task_key=TASK_KEY_PARENT)

    assert not TaskClosed(when=NOW) in event_store.events_for(key=TASK_KEY_PARENT)
    assert response == Err(TaskHavingOpenedSubTask())


@pytest.mark.parametrize("title, aggregate_events", [
    ["with_one_closed_sub_task", [
        AggregateEvent(key=TASK_KEY_PARENT, events=[
            TaskOpened(when=PREVIOUSLY), SubTaskAttached(task_key=TASK_KEY_CHILD_ONE, when=PREVIOUSLY)]),
        AggregateEvent(key=TASK_KEY_CHILD_ONE, events=[
            TaskOpened(when=PREVIOUSLY), TaskClosed(when=PREVIOUSLY)])]
     ],
    ["with two_closed tasks", [
        AggregateEvent(key=TASK_KEY_PARENT, events=[
            TaskOpened(when=PREVIOUSLY),
            SubTaskAttached(task_key=TASK_KEY_CHILD_ONE, when=PREVIOUSLY),
            SubTaskAttached(task_key=TASK_KEY_CHILD_TWO, when=PREVIOUSLY)]),

        AggregateEvent(key=TASK_KEY_CHILD_ONE, events=[
            TaskOpened(when=PREVIOUSLY), TaskClosed(when=PREVIOUSLY)]),
        AggregateEvent(key=TASK_KEY_CHILD_TWO, events=[
            TaskOpened(when=PREVIOUSLY), TaskClosed(when=PREVIOUSLY)])]
     ]
])
def test_close_task_having_only_closed_sub_task(title: str, aggregate_events: list[AggregateEvent[Event]], sut: TodolistUseCasePort,
                                                event_store: EventStoreInMemory) -> None:
    event_store.save(*aggregate_events)
    event_store.save()

    response = sut.close_task(task_key=TASK_KEY_PARENT)

    assert TaskClosed(when=NOW) in event_store.events_for(key=TASK_KEY_PARENT)
    assert response == Ok(None)
