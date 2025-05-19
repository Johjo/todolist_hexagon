from abc import abstractmethod, ABC
from typing import Callable
from uuid import UUID

from datetime_provider import DateTimeProviderPrimaryPort

from todolist_hexagon.base.events import EventList
from todolist_hexagon.base.ports import EventStorePort, AggregateEvent
from todolist_hexagon.commands import CreateTodolist, AttachTask, OpenTask, CloseTask, AttachSubTask, \
    DescribeTask
from todolist_hexagon.events import Event
from todolist_hexagon.result import Result, Ok
from todolist_hexagon.task_aggregate import Task
from todolist_hexagon.task_error import TaskError
from todolist_hexagon.todolist_aggregate import Todolist


class TodolistUseCasePort(ABC):
    @abstractmethod
    def create_todolist(self, todolist_key: UUID) -> None:
        pass

    @abstractmethod
    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        pass

    @abstractmethod
    def close_task(self, task_key: UUID) -> Result[None, TaskError]:
        pass

    @abstractmethod
    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
        pass

    @abstractmethod
    def describe_task(self, *, task_key: UUID, title: str | None = None, description: str | None = None) -> Result[None, TaskError]:
        pass


class TodolistUseCase(TodolistUseCasePort):
    def __init__(self, event_store: EventStorePort[Event], datetime_provider: DateTimeProviderPrimaryPort) -> None:
        self._datetime_provider = datetime_provider
        self.event_store = event_store

    def create_todolist(self, todolist_key: UUID) -> None:
        todolist = Todolist(self.event_store.events_for(todolist_key))
        events = todolist.decide(CreateTodolist(key=todolist_key, when=self._datetime_provider.now()))
        self.event_store.save(AggregateEvent(key=todolist_key, events=events))

    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        when = self._datetime_provider.now()
        task_events = (Task(task_key=task_key, event_store=self.event_store)
                       .decide(OpenTask(task_key=task_key, title=title, description=description, when=when)))
        todolist_event = Todolist(events=[]).decide(AttachTask(task_key=task_key, when=when))

        self.event_store.save(AggregateEvent(key=task_key, events=task_events.unwrap()), AggregateEvent(key=todolist_key, events=todolist_event))

    def close_task(self, task_key: UUID) -> Result[None, TaskError]:
        when = self._datetime_provider.now()
        return (
            Task(task_key=task_key, event_store=self.event_store)
            .decide(CloseTask(task_key=task_key, when=when))
            .and_then(self._save_events(task_key))
        )

    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
        now = self._datetime_provider.now()
        children_task_events = Task(task_key=children_task_key, event_store=self.event_store).decide(
            OpenTask(task_key=children_task_key, title=title, description=description, when=now))
        parent_task_events = Task(task_key=parent_task_key, event_store=self.event_store).decide(
            AttachSubTask(task_key=children_task_key, when=now))
        self.event_store.save(AggregateEvent(key=children_task_key, events=children_task_events.unwrap()), AggregateEvent(key=parent_task_key, events=parent_task_events.unwrap()))

    def describe_task(self, *, task_key: UUID, title: str | None = None, description: str | None = None) -> Result[None, TaskError]:
        now = self._datetime_provider.now()

        return (
            Task(task_key=task_key, event_store=self.event_store)
            .decide(DescribeTask(title=title, description=description, when=now))
            .and_then(self._save_events(task_key))
        )

    def _save_events(self, key: UUID) -> Callable[[EventList[Event]], 'Result[None, TaskError]']:
        def _save(events: EventList[Event]) -> Result[None, TaskError]:
            self.event_store.save(AggregateEvent(key=key, events=events))
            return Ok(None)

        return _save