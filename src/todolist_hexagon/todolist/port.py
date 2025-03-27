from abc import ABC, abstractmethod

from expression import Option

from src.todolist_hexagon.shared.type import TaskKey, TodolistName, TodolistKey
from src.todolist_hexagon.todolist.aggregate import TodolistSnapshot


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
