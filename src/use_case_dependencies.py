from typing import Protocol

from src.todolist_hexagon.todolist.port import TodolistSetPort
from src.todolist_hexagon.todolist.write.close_task import CloseTaskPrimaryPort, CloseTaskUseCase
from src.todolist_hexagon.todolist.write.create_todolist import TodolistCreate
from src.todolist_hexagon.todolist.write.import_many_task import ImportManyTask, TaskKeyGeneratorPort
from src.todolist_hexagon.todolist.write.open_task import OpenTaskUseCase
from src.todolist_hexagon.todolist.write.postpone_task import PostPoneTask
from src.todolist_hexagon.todolist.write.reword_task import RewordTask
from src.todolist_hexagon.todolist.write.todolist_delete import TodolistDelete


class AdapterDependenciesPort(Protocol):
    def todolist_set(self) -> TodolistSetPort: ...

    def task_key_generator(self) -> TaskKeyGeneratorPort: ...


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
