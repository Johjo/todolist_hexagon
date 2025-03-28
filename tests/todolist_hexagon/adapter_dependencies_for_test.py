from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest


class AdapterDependenciesDummy:
    def task_key_generator(self) -> TaskKeyGeneratorForTest:
        raise Exception("not implemented")


class AdapterDependenciesForTest(AdapterDependenciesDummy):
    def __init__(self,
                 todolist_set: TodolistSetForTest | None = None,
                 task_key_generator: TaskKeyGeneratorForTest | None = None,
                 fvp_session_set: FvpSessionSetPort | None = None):

        self._todolist_set = todolist_set
        self._task_key_generator = task_key_generator
        self._session_set = fvp_session_set

    def todolist_set(self) -> TodolistSetForTest:
        if not self._todolist_set:
            raise Exception(f"todolist_set not defined")
        return self._todolist_set

    def task_key_generator(self) -> TaskKeyGeneratorForTest:
        if not self._task_key_generator:
            raise Exception(f"task_key_generator not defined")
        return self._task_key_generator

    def session_set(self) -> FvpSessionSetPort:
        if not self._session_set:
            raise Exception("fvp session set not defined")
        return self._session_set
