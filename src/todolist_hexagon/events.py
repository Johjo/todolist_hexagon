from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TodoListCreated:
    todolist_key: UUID


@dataclass(frozen=True, eq=True)
class TaskOpened:
    pass


@dataclass
class TaskAttached:
    task_key: UUID

@dataclass
class TaskDescribed:
    title: str
    description: str


TaskEvent = TaskOpened | TaskAttached | TaskDescribed
Event = TodoListCreated | TaskEvent
EventList = list[Event]
