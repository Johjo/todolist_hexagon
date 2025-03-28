from expression import Result

from todolist_hexagon.shared.type import TodolistKey, TaskKey, TaskName
from todolist_hexagon.todolist.aggregate import TodolistAggregate
from todolist_hexagon.todolist.port import TodolistSetPort
from todolist_hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class RewordTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, task_key: TaskKey, new_wording: TaskName):
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.reword_task(task_key, new_wording)

        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_key, update)
