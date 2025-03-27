from expression import Result, pipe

from src.dependencies import Dependencies
from src.hexagon.shared.type import TodolistName, TaskKey, TaskExecutionDate, TodolistKey
from src.hexagon.todolist.aggregate import TodolistAggregate
from src.hexagon.todolist.port import TodolistSetPort
from src.hexagon.todolist.todolist_repository import TodolistRepository
from src.hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class PostPoneTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, key: TaskKey, execution_date: TaskExecutionDate):
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.postpone_task(key, execution_date)

        updater = UpdateTodolistAggregate(todolist_set=self._todolist_set)
        return updater.execute(todolist_key, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'PostPoneTask':
        todolist_set = dependencies.get_adapter(TodolistSetPort)
        return PostPoneTask(todolist_set)
