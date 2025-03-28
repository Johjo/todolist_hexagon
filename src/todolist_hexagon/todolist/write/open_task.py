from expression import Result, Nothing

from todolist_hexagon.shared.type import TaskName, TaskOpen, TodolistKey, TaskKey
from todolist_hexagon.todolist.aggregate import Task, TodolistAggregate
from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class OpenTaskUseCase:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, task_key: TaskKey, name: TaskName) -> Result[None, str]:
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.open_task(Task(key=task_key, name=name, is_open=TaskOpen(True), execution_date=Nothing))

        updater = UpdateTodolistAggregate(todolist_set=self._todolist_set)
        return updater.execute(todolist_key, update)
