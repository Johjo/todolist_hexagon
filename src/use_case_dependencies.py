from typing import Protocol

from src.todolist_hexagon.fvp.aggregate import FvpSessionSetPort
from src.todolist_hexagon.fvp.write.cancel_priority import CancelPriority
from src.todolist_hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from src.todolist_hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from src.todolist_hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from src.todolist_hexagon.todolist.write.close_task import CloseTaskPrimaryPort, CloseTaskUseCase
from src.todolist_hexagon.todolist.write.create_todolist import TodolistCreate
from src.todolist_hexagon.todolist.write.import_many_task import ImportManyTask
from src.todolist_hexagon.todolist.write.open_task import OpenTaskUseCase
from src.todolist_hexagon.todolist.write.postpone_task import PostPoneTask
from src.todolist_hexagon.todolist.write.reword_task import RewordTask
from src.todolist_hexagon.todolist.write.todolist_delete import TodolistDelete


class AdapterDependenciesPort(Protocol):
    def todolist_set(self) -> TodolistSetPort: ...

    def task_key_generator(self) -> TaskKeyGeneratorPort: ...

    def session_set(self) -> FvpSessionSetPort: ...


class UseCaseDependencies:
    def __init__(self, adapter_dependencies: AdapterDependenciesPort):
        self._adapter_dependencies = adapter_dependencies

    def close_task(self) -> CloseTaskPrimaryPort:
        return CloseTaskUseCase(todolist_set=(self._adapter_dependencies.todolist_set()))

    def create_todolist(self) -> TodolistCreate:
        return TodolistCreate(todolist_set=(self._adapter_dependencies.todolist_set()))

    def delete_todolist(self) -> TodolistDelete:
        return TodolistDelete(todolist_set=(self._adapter_dependencies.todolist_set()))

    def import_many_task(self) -> ImportManyTask:
        return ImportManyTask(todolist_set=(self._adapter_dependencies.todolist_set()),
                              task_key_generator=(self._adapter_dependencies.task_key_generator()))

    def open_task(self) -> OpenTaskUseCase:
        return OpenTaskUseCase(todolist_set=self._adapter_dependencies.todolist_set())

    def postpone_task(self) -> PostPoneTask:
        return PostPoneTask(todolist_set=self._adapter_dependencies.todolist_set())

    def reword_task(self) -> RewordTask:
        return RewordTask(todolist_set=self._adapter_dependencies.todolist_set())

    def cancel_priority(self) -> CancelPriority:
        return CancelPriority(session_set=self._adapter_dependencies.session_set())

    def choose_and_ignore_task(self) -> ChooseAndIgnoreTaskFvp:
        return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions=self._adapter_dependencies.session_set())

    def reset_fvp_session(self) -> ResetFvpSession:
        return ResetFvpSession(set_of_fvp_sessions=self._adapter_dependencies.session_set())
