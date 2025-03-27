from expression import Result

from src.dependencies import Dependencies
from src.todolist_hexagon.shared.type import TaskKey, TaskExecutionDate, TodolistKey
from src.todolist_hexagon.todolist.aggregate import TodolistAggregate
from src.todolist_hexagon.todolist.port import TodolistSetPort
from src.todolist_hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


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
