from abc import abstractmethod, ABC
from typing import Protocol

from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort


class WriteAdapterDependenciesPort(ABC):
    @abstractmethod
    def todolist_set(self) -> TodolistSetPort: ...

    @abstractmethod
    def task_key_generator(self) -> TaskKeyGeneratorPort: ...

    @abstractmethod
    def fvp_session_set(self) -> FvpSessionSetPort: ...
