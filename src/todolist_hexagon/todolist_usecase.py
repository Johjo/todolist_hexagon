from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from todolist_hexagon.commands import CreateTodolist, AttachTask
from todolist_hexagon.events import TaskOpened, EventList
from todolist_hexagon.ports import EventStorePort, AggregateEvent
from todolist_hexagon.todolist_aggregate import Todolist


@dataclass
class OpenTask:
    task_key: UUID
    title: str
    description: str


class Task:
    def decide(self, command: OpenTask) -> EventList:
        return [TaskOpened(title=command.title, description=command.description)]


class TodolistUseCasePort:
    @abstractmethod
    def create_todolist(self, todolist_key: UUID) -> None:
        pass

    @abstractmethod
    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        pass


class TodolistUseCase(TodolistUseCasePort):
    def __init__(self, event_store: EventStorePort) -> None:
        self.event_store = event_store

    def create_todolist(self, todolist_key: UUID) -> None:
        todolist = Todolist(self.event_store.events_for(todolist_key))
        events = todolist.decide(CreateTodolist(todolist_key))
        self.event_store.save(AggregateEvent(key=todolist_key, events=events))

    def open_task(self, todolist_key: UUID, task_key: UUID, title: str, description: str) -> None:
        task_events = Task().decide(OpenTask(task_key=task_key, title=title, description=description))
        todolist_event = Todolist(events=[]).decide(AttachTask(task_key=task_key))

        self.event_store.save(AggregateEvent(key=task_key, events=task_events), AggregateEvent(key=todolist_key, events=todolist_event))
