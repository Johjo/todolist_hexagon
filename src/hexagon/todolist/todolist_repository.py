from expression import Result, pipe

from src.hexagon.shared.event import Event
from src.hexagon.shared.type import TodolistName
from src.hexagon.todolist.aggregate import TodolistAggregate, TodolistSnapshot
from src.hexagon.todolist.port import TodolistSetPort


class TodolistRepository:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def load_todolist(self, todolist_name: TodolistName) -> Result[TodolistAggregate, str]:
        return pipe(todolist_name, self._load_snapshot, self._from_snapshot)

    def save_todolist(self, aggregate: Result[TodolistAggregate, str]) -> Result[tuple[Event, ...], str]:
        return pipe(aggregate,
                    self._save_snapshot,
                    self._to_events
                    )

    @staticmethod
    def _from_snapshot(snapshot: Result[TodolistSnapshot, str]) -> Result[TodolistAggregate, str]:
        return snapshot.map(TodolistAggregate.from_snapshot)

    def _load_snapshot(self, todolist_name: TodolistName) -> Result[TodolistSnapshot, str]:
        return self._todolist_set.by(todolist_name).to_result(error="todolist not found")

    def _save_snapshot(self, todolist: Result[TodolistAggregate, str]) -> Result[TodolistAggregate, str]:
        return (todolist
                .map(lambda _todolist: self._todolist_set.save_snapshot(_todolist.to_snapshot()))
                .bind(lambda _: todolist))

    @staticmethod
    def _to_events(todolist: Result[TodolistAggregate, str]) -> Result[tuple[Event, ...], str]:
        return todolist.map(lambda _todolist: _todolist.uncommited_events())