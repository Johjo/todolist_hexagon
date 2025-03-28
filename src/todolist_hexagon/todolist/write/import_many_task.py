from abc import ABC, abstractmethod
from dataclasses import dataclass

from expression import Result, Option

from todolist_hexagon.shared.type import TaskKey, TaskName, TaskOpen, TaskExecutionDate, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistAggregate, TaskSnapshot
from todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from todolist_hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


@dataclass(frozen=True)
class TaskImported:
    name: TaskName
    is_open: TaskOpen
    execution_date: Option[TaskExecutionDate]

    def to_snapshot(self, key: TaskKey) -> TaskSnapshot:
        return TaskSnapshot(key=key, name=self.name, is_open=self.is_open, execution_date=self.execution_date)


class ExternalTodoListPort(ABC):
    @abstractmethod
    def all_tasks(self) -> list[TaskImported]:
        pass


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort, task_key_generator: TaskKeyGeneratorPort):
        self._todolist_set = todolist_set
        self._task_key_generator = task_key_generator

    def execute(self, todolist_key: TodolistKey, external_todolist: ExternalTodoListPort):
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.import_tasks([task.to_snapshot(self._task_key_generator.generate()) for task in external_todolist.all_tasks()])

        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_key, update)
