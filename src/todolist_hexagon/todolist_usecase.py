from abc import abstractmethod, ABC
from uuid import UUID

from datetime_provider import DateTimeProviderPrimaryPort

from todolist_hexagon.commands import CreateTodolist, AttachTask, OpenTask, CloseTask, TaskCommand, AttachSubTask
from todolist_hexagon.events import TaskOpened, TaskDescribed, TaskClosed, SubTaskAttached, Event
from todolist_hexagon.base.events import EventList
from todolist_hexagon.base.ports import EventStorePort, AggregateEvent
from todolist_hexagon.todolist_aggregate import Todolist


class Task:
    def decide(self, command: TaskCommand) -> EventList[Event]:
        match command:
            case OpenTask(title=title, description=description, when=when):
                return [TaskDescribed(title=title, description=description, when=when), TaskOpened(when=when)]

            case CloseTask(when=when):
                return [TaskClosed(when=when)]

            case AttachSubTask(task_key=task_key, when=when):
                return [SubTaskAttached(task_key=task_key, when=when)]

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

    @abstractmethod
    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
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
        task_events = Task().decide(OpenTask(task_key=task_key, title=title, description=description, when=when))
        todolist_event = Todolist(events=[]).decide(AttachTask(task_key=task_key, when=when))

        self.event_store.save(AggregateEvent(key=task_key, events=task_events), AggregateEvent(key=todolist_key, events=todolist_event))

    def close_task(self, task_key: UUID) -> None:
        when = self._datetime_provider.now()
        task_events = Task().decide(CloseTask(task_key=task_key, when=when))
        self.event_store.save(AggregateEvent(key=task_key, events=task_events))

    def open_sub_task(self, parent_task_key: UUID, children_task_key: UUID, title: str, description: str) -> None:
        when = self._datetime_provider.now()
        children_task_events = Task().decide(OpenTask(task_key=children_task_key, title=title, description=description, when=when))
        parent_task_events = Task().decide(AttachSubTask(task_key=children_task_key, when=when))
        self.event_store.save(AggregateEvent(key=children_task_key, events=children_task_events), AggregateEvent(key=parent_task_key, events=parent_task_events))