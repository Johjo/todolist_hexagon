from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from src.hexagon.shared.type import TodolistKey, UserKey, TodolistName


@dataclass(frozen=True)
class TodolistSnapshot:
    key: TodolistKey
    name: TodolistName


@dataclass(frozen=True)
class UserSnapshot:
    key: UserKey
    todolist: Tuple[TodolistSnapshot, ...]


class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: UserSnapshot) -> None:
        pass

    @abstractmethod
    def by_user(self, key: UserKey) -> UserSnapshot | None:
        pass


