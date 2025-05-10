from dataclasses import dataclass
from uuid import UUID

from todolist_hexagon.base.events import EventBase


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

@dataclass(frozen=True)
class SubTaskAttached(EventBase):
    task_key: UUID


TaskEvent = TaskOpened |  TaskDescribed | TaskClosed | SubTaskAttached
TodolistEvent = TodoListCreated | TaskAttached
Event = TodolistEvent | TaskEvent


