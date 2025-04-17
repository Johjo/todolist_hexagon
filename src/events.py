from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TodoListCreated:
    key: UUID


EventList = list[TodoListCreated]
