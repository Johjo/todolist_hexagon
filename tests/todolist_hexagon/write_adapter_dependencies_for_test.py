from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort


class WriteAdapterDependenciesForTest(WriteAdapterDependenciesPort):
    def __init__(self, todolist_set: TodolistSetPort | None = None, fvp_session_set: FvpSessionSetPort | None = None,
                 task_key_generator: TaskKeyGeneratorPort | None = None):
        self._task_key_generator = task_key_generator
        self._fvp_session_set = fvp_session_set
        self._todolist_set = todolist_set

    def task_key_generator(self) -> TaskKeyGeneratorPort:
        if not self._task_key_generator:
            raise Exception("task_key_generator not defined")
        return self._task_key_generator

    def fvp_session_set(self) -> FvpSessionSetPort:
        if not self._fvp_session_set:
            raise Exception("fvp session set not defined")
        return self._fvp_session_set

    def todolist_set(self) -> TodolistSetPort:
        if not self._todolist_set:
            raise Exception("todolist_set not defined")
        return self._todolist_set
