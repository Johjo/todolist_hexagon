from expression import Result, pipe

from src.hexagon.shared.type import TodolistName, TodolistKey
from src.hexagon.todolist.aggregate import TodolistAggregate, TodolistSnapshot
from src.hexagon.todolist.port import TodolistSetPort


class UpdateTodolistAggregate:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, update) -> Result[None, str]:
        return pipe(
            todolist_key,
            self.load_snapshot,
            lambda snapshot: snapshot.map(TodolistAggregate.from_snapshot),
            lambda todolist: todolist.bind(update),
            lambda todolist: todolist.map(self.to_snapshot),
            lambda snapshot: snapshot.map(self.save_snapshot)
        )

    def load_snapshot(self, todolist_key: TodolistKey) -> Result[TodolistSnapshot, str]:
        return self._todolist_set.by(todolist_key=todolist_key).to_result(error="todolist not found")

    @staticmethod
    def to_snapshot(aggregate: TodolistAggregate) -> TodolistSnapshot:
        return aggregate.to_snapshot()

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        self._todolist_set.save_snapshot(snapshot)
