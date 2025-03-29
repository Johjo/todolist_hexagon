from typing import Protocol

from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort


class WriteAdapterDependenciesPort(Protocol):
    def todolist_set(self) -> TodolistSetPort: ...

    def task_key_generator(self) -> TaskKeyGeneratorPort: ...

    def session_set(self) -> FvpSessionSetPort: ...
