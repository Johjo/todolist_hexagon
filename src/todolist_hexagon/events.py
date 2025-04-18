from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TodoListCreated:
    todolist_key: UUID


@dataclass(frozen=True, eq=True)
class TaskOpened:
    title: str
    description: str


@dataclass
class TaskAttached:
    task_key: UUID

Event = TodoListCreated | TaskOpened | TaskAttached
EventList = list[Event]
