from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class EventBase:
    when: datetime

@dataclass(frozen=True, eq=True)
class TodoListCreated(EventBase):
    pass


@dataclass(frozen=True, eq=True)
class TaskOpened(EventBase):
    pass

@dataclass(frozen=True)
class TaskClosed(EventBase):
    pass


@dataclass(frozen=True)
class TaskAttached(EventBase):
    task_key: UUID

@dataclass(frozen=True)
class TaskDescribed(EventBase):
    title: str
    description: str


TaskEvent = TaskOpened |  TaskDescribed | TaskClosed
TodolistEvent = TodoListCreated | TaskAttached
Event = TodolistEvent | TaskEvent
EventList = list[Event]


