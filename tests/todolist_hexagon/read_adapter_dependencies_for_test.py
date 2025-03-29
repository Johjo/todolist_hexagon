from todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort
from todolist_hexagon.read_adapter_dependencies import ReadAdapterDependenciesPort


class ReadAdapterDependenciesForTest(ReadAdapterDependenciesPort):
    def __init__(self, todolist: TodolistPort | None = None, fvp_session_set: FvpSessionSetPort | None = None):
        self._fvp_session_set = fvp_session_set
        self._todolist = todolist

    def todolist(self) -> TodolistPort:
        if not self._todolist:
            raise Exception("todolist not defined")
        return self._todolist

    def fvp_session_set(self) -> FvpSessionSetPort:
        if not self._fvp_session_set:
            raise Exception("fvp session set not defined")
        return self._fvp_session_set
