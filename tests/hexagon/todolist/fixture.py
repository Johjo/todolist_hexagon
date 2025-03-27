from uuid import UUID

from expression import Option, Nothing, Some

from src.hexagon.shared.type import TaskKey, TodolistKey
from src.hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot
from src.hexagon.todolist.port import TodolistSetPort
from src.hexagon.todolist.write.import_many_task import TaskKeyGeneratorPort
from tests.fixture import TaskBuilder, TodolistBuilder


class TodolistSetForTest(TodolistSetPort):
    def __init__(self) -> None:
        self._all_snapshot: dict[TodolistKey, Option[TodolistSnapshot]] = {}

    def by(self, todolist_key: TodolistKey) -> Option[TodolistSnapshot]:
        if todolist_key not in self._all_snapshot:
            return Nothing
        return self._all_snapshot[todolist_key]

    def save_snapshot(self, todolist: TodolistSnapshot) -> None:
        self._all_snapshot[todolist.key] = Some(todolist)

    def feed(self, todolist: TodolistBuilder):
        self._all_snapshot[todolist.to_key()] = Some(todolist.to_snapshot())

    def feed_nothing(self, todolist_key: UUID):
        self._all_snapshot[TodolistKey(todolist_key)] = Nothing

    def delete(self, todolist_key):
        del self._all_snapshot[todolist_key]


class TaskKeyGeneratorForTest(TaskKeyGeneratorPort):
    def __init__(self) -> None:
        self.keys: list[TaskKey] | None = None

    def feed(self, *items: TaskKey | TaskSnapshot | TaskBuilder) -> None:
        self.keys = [self._key_from(item) for item in items]

    def generate(self) -> TaskKey:
        if not self.keys:
            raise Exception("key must be fed before generating")
        return self.keys.pop(0)

    @staticmethod
    def _key_from(item: TaskKey | TaskSnapshot | TaskBuilder):
        if isinstance(item, TaskSnapshot):
            return item.key
        if isinstance(item, TaskBuilder):
            return item.key

        return item
