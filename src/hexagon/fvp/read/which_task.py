from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from expression import Option, Nothing

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import Task, FinalVersionPerfectedSession, NothingToDo, DoTheTask, ChooseTheTask, \
    FvpSessionSetPort
from src.hexagon.shared.type import UserKey, TodolistKey
from src.shared.filter import TextFilter


@dataclass(frozen=True, eq=True)
class WhichTaskFilter:
    todolist_key: UUID
    reference_date: date
    include_context: tuple[str, ...] = ()
    exclude_context: tuple[str, ...] = ()

    def include(self, task_name: str, task_date: Option[date]) -> bool:
        if task_date != Nothing:
            if task_date.value > self.reference_date:
                return False
        text_filter = TextFilter(included_words=self.include_context, excluded_words=self.exclude_context)
        return text_filter.include(task_name)


class TodolistPort(ABC):
    @abstractmethod
    def all_open_tasks(self, user_key: UserKey, task_filter: WhichTaskFilter) -> list[Task]:
        pass


class WhichTaskQuery:
    def __init__(self, todolist: TodolistPort, fvp_sessions_set: FvpSessionSetPort):
        self._fvp_sessions_set = fvp_sessions_set
        self._todolist = todolist

    def which_task(self, user_key: UserKey, task_filter: WhichTaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        session : FinalVersionPerfectedSession= self._get_or_create_session(user_key=user_key)
        open_tasks = self._todolist.all_open_tasks(user_key=user_key, task_filter=task_filter)
        return session.which_task(open_tasks)

    def _get_or_create_session(self, user_key: UserKey) -> FinalVersionPerfectedSession:
        snapshot = self._fvp_sessions_set.by(user_key=user_key)
        return FinalVersionPerfectedSession.from_snapshot(snapshot)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'WhichTaskQuery':
        return WhichTaskQuery(dependencies.get_adapter(TodolistPort), dependencies.get_adapter(FvpSessionSetPort))

