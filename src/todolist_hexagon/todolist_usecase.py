from abc import abstractmethod, ABC
from dataclasses import dataclass, replace
from typing import Callable, assert_never, cast
from uuid import UUID

from datetime_provider import DateTimeProviderPrimaryPort

from todolist_hexagon.base.events import EventList
from todolist_hexagon.base.ports import EventStorePort, AggregateEvent
from todolist_hexagon.commands import CreateTodolist, AttachTask, OpenTask, CloseTask, TaskCommand, AttachSubTask, \
    DescribeTask
from todolist_hexagon.events import TaskOpened, TaskDescribed, TaskClosed, SubTaskAttached, Event, TaskEvent
from todolist_hexagon.result import Result, Ok, Err
from todolist_hexagon.todolist_aggregate import Todolist


@dataclass(frozen=True)
class TaskNotFound:
    pass

@dataclass(frozen=True)
class TaskAlreadyClosed:
    pass

TaskError = TaskNotFound | TaskAlreadyClosed


@dataclass(frozen=True, eq=True)
class TaskState:
    exist: bool = False
    is_closed: bool = False

    def evolve(self, event: TaskEvent) -> 'TaskState':
        match event:
            case TaskDescribed():
                pass
            case TaskClosed():
                return replace(self, is_closed=True, exist=True)

            case TaskOpened():
                pass
            case SubTaskAttached():
                pass

            case _:
                assert_never(event)

        return TaskState(exist=True)


class Task:
    def __init__(self, history: EventList[Event]) -> None:
        self.state = TaskState()
        for event in history:
            self.state = self.state.evolve(cast(TaskEvent, event))


    def decide(self, command: TaskCommand) -> Result[EventList[Event], TaskNotFound | TaskAlreadyClosed]:
        match command:
            case OpenTask(title=title, description=description, when=when):
                return Ok([TaskDescribed(title=title, description=description, when=when), TaskOpened(when=when)])

            case CloseTask(when=when):
                if not self.state.exist:
                    return Err(TaskNotFound())
                if self.state.is_closed:
                    return Err(TaskAlreadyClosed())
                return Ok([TaskClosed(when=when)])

            case AttachSubTask(task_key=task_key, when=when):
                return Ok([SubTaskAttached(task_key=task_key, when=when)])

            case DescribeTask(title=title, description=description, when=when):
                if self.state.exist:
                    return Ok([TaskDescribed(title=title, description=description, when=when)])
                return Err(TaskNotFound())

            case _:
                raise NotImplementedError(command)


class TodolistUseCasePort(ABC):
    @abstractmethod
    def create_todolist(self, todolist_key: UUID) -> None:
        pass

    @abstractmethod
    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        pass

    @abstractmethod
    def close_task(self, task_key: UUID) -> Result[None, TaskNotFound | TaskAlreadyClosed]:
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
        task_events = Task(self.event_store.events_for(key=task_key)).decide(OpenTask(task_key=task_key, title=title, description=description, when=when))
        todolist_event = Todolist(events=[]).decide(AttachTask(task_key=task_key, when=when))

        self.event_store.save(AggregateEvent(key=task_key, events=task_events.unwrap()), AggregateEvent(key=todolist_key, events=todolist_event))

    def close_task(self, task_key: UUID) -> Result[None, TaskError]:
        when = self._datetime_provider.now()
        return (
            Task(self.event_store.events_for(key=task_key))
            .decide(CloseTask(task_key=task_key, when=when))
            .and_then(self._save_events(task_key))
        )

    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
        now = self._datetime_provider.now()
        children_task_events = Task(self.event_store.events_for(key=children_task_key)).decide(OpenTask(task_key=children_task_key, title=title, description=description, when=now))
        parent_task_events = Task(self.event_store.events_for(key=parent_task_key)).decide(AttachSubTask(task_key=children_task_key, when=now))
        self.event_store.save(AggregateEvent(key=children_task_key, events=children_task_events.unwrap()), AggregateEvent(key=parent_task_key, events=parent_task_events.unwrap()))

    def describe_task(self, *, task_key: UUID, title: str | None = None, description: str | None = None) -> Result[None, TaskError]:
        now = self._datetime_provider.now()

        return (
            Task(self.event_store.events_for(key=task_key))
            .decide(DescribeTask(title=title, description=description, when=now))
            .and_then(self._save_events(task_key))
        )

    def _save_events(self, key: UUID) -> Callable[[EventList[Event]], 'Result[None, TaskError]']:
        def _save(events: EventList[Event]) -> Result[None, TaskError]:
            self.event_store.save(AggregateEvent(key=key, events=events))
            return Ok(None)

        return _save