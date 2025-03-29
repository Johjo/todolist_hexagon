from abc import ABC, abstractmethod

from typing_extensions import Protocol

from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort


class ReadAdapterDependenciesPort(ABC):

    @abstractmethod
    def todolist(self) -> TodolistPort: ...

    @abstractmethod
    def fvp_session_set(self) -> FvpSessionSetPort: ...
