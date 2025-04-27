from abc import abstractmethod, ABC
from datetime import datetime
from uuid import UUID

from todolist_hexagon.commands import CreateTodolist, AttachTask, OpenTask, CloseTask, TaskCommand
from todolist_hexagon.events import TaskOpened, EventList, TaskDescribed, TaskClosed
from todolist_hexagon.ports import EventStorePort, AggregateEvent
from todolist_hexagon.todolist_aggregate import Todolist


class Task:
    def decide(self, command: TaskCommand) -> EventList:
        match command:
            case OpenTask(title=title, description=description, when=when):
                return [TaskDescribed(title=title, description=description, when=when), TaskOpened(when=when)]

            case CloseTask(when=when):
                return [TaskClosed(when=when)]
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
    def close_task(self, task_key: UUID) -> None:
        pass


class DateTimeProviderPort(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass


class TodolistUseCase(TodolistUseCasePort):
    def __init__(self, event_store: EventStorePort, datetime_provider: DateTimeProviderPort) -> None:
        self._datetime_provider = datetime_provider
        self.event_store = event_store

    def create_todolist(self, todolist_key: UUID) -> None:
        todolist = Todolist(self.event_store.events_for(todolist_key))
        events = todolist.decide(CreateTodolist(key=todolist_key, when=self._datetime_provider.now()))
        self.event_store.save(AggregateEvent(key=todolist_key, events=events))

    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        when = self._datetime_provider.now()
        task_events = Task().decide(OpenTask(task_key=task_key, title=title, description=description, when=when))
        todolist_event = Todolist(events=[]).decide(AttachTask(task_key=task_key, when=when))

        self.event_store.save(AggregateEvent(key=task_key, events=task_events), AggregateEvent(key=todolist_key, events=todolist_event))

    def close_task(self, task_key: UUID) -> None:
        when = self._datetime_provider.now()
        task_events = Task().decide(CloseTask(task_key=task_key, when=when))
        self.event_store.save(AggregateEvent(key=task_key, events=task_events))
