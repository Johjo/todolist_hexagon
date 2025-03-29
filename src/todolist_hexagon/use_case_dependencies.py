from todolist_hexagon.fvp.write.cancel_priority import CancelPriority
from todolist_hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from todolist_hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from todolist_hexagon.todolist.write.close_task import CloseTaskPrimaryPort, CloseTaskUseCase
from todolist_hexagon.todolist.write.create_todolist import TodolistCreate
from todolist_hexagon.todolist.write.import_many_task import ImportManyTask
from todolist_hexagon.todolist.write.open_task import OpenTaskUseCase
from todolist_hexagon.todolist.write.postpone_task import PostPoneTask
from todolist_hexagon.todolist.write.reword_task import RewordTask
from todolist_hexagon.todolist.write.todolist_delete import TodolistDelete
from todolist_hexagon.write_adapter_dependencies import WriteAdapterDependenciesPort


class UseCaseDependencies:
    def __init__(self, adapter_dependencies: WriteAdapterDependenciesPort):
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
        return CancelPriority(session_set=self._adapter_dependencies.fvp_session_set())

    def choose_and_ignore_task(self) -> ChooseAndIgnoreTaskFvp:
        return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions=self._adapter_dependencies.fvp_session_set())

    def reset_fvp_session(self) -> ResetFvpSession:
        return ResetFvpSession(set_of_fvp_sessions=self._adapter_dependencies.fvp_session_set())
