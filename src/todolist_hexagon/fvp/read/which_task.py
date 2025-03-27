from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from expression import Option, Nothing


from src.todolist_hexagon.fvp.aggregate import Task, FinalVersionPerfectedSession, NothingToDo, DoTheTask, ChooseTheTask, \
    FvpSessionSetPort
from src.todolist_hexagon.shared.type import UserKey, TodolistKey


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


class TextFilter:
    def __init__(self, included_words: tuple[str, ...], excluded_words: tuple[str, ...]):
        self._included_words = included_words
        self._excluded_words = excluded_words

    def include(self, text: str) -> bool:
        if not self.match_included_words(text):
            return False

        if self.match_excluded_words(text):
            return False

        return True

    def match_included_words(self, text: str) -> bool:
        if self._included_words == ():
            return True

        for included_word in self._included_words:
            if any(included_word == word for word in text.split()):
                return True
        return False

    def match_excluded_words(self, text: str) -> bool:
        for excluded_word in self._excluded_words:
            if any(excluded_word == word for word in text.split()):
                return True
        return False
