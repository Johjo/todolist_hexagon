from abc import ABC, abstractmethod

from expression import Result

from todolist_hexagon.shared.type import TaskKey, TodolistKey
from todolist_hexagon.todolist.aggregate import TodolistAggregate
from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class CloseTaskPrimaryPort(ABC):
    @abstractmethod
    def execute(self, todolist_key: TodolistKey, task_key: TaskKey) -> Result[None, str]:
        pass


class CloseTaskUseCase(CloseTaskPrimaryPort):
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, task_key: TaskKey) -> Result[None, str]:
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.close_task(task_key)

        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_key, update)
