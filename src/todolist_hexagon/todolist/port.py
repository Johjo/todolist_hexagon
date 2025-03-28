from abc import ABC, abstractmethod

from expression import Option

from todolist_hexagon.shared.type import TaskKey, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistSnapshot


class TodolistSetPort(ABC):
    @abstractmethod
    def by(self, todolist_key: TodolistKey) -> Option[TodolistSnapshot]:
        pass

    @abstractmethod
    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        pass

    @abstractmethod
    def delete(self, todolist_key: TodolistKey) -> None:
        pass


class TaskKeyGeneratorPort(ABC):
    @abstractmethod
    def generate(self) -> TaskKey:
        pass
