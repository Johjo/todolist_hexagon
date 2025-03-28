from expression import Result, Nothing, Error, Ok

from todolist_hexagon.shared.type import TodolistName, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistAggregate
from todolist_hexagon.todolist.port import TodolistSetPort


class TodolistCreate:
    def __init__(self, todolist_set: TodolistSetPort) -> None:
        self._todolist_set: TodolistSetPort = todolist_set

    def execute(self, todolist_key: TodolistKey, todolist_name: TodolistName) -> Result[None, None]:
        if self._todolist_set.by(todolist_key=todolist_key) != Nothing:
            return Error(None)

        self._todolist_set.save_snapshot(TodolistAggregate.create(todolist_key=todolist_key, todolist_name=todolist_name).to_snapshot())
        return Ok(None)
