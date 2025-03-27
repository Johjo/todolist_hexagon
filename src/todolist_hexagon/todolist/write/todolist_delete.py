from expression import Result, Ok

from src.todolist_hexagon.shared.type import TodolistKey
from src.todolist_hexagon.todolist.port import TodolistSetPort


class TodolistDelete:
    def __init__(self, todolist_set: TodolistSetPort) -> None:
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey) -> Result[None, None]:
        self._todolist_set.delete(todolist_key=todolist_key)
        return Ok(None)
