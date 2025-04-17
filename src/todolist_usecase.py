from uuid import UUID

from src.ports import EventStore
from src.todolist_aggregate import Todolist
from src.commands import CreateTodolist


class TodolistUseCase:
    def __init__(self, event_store: EventStore) -> None:
        self.event_store = event_store

    def create_todolist(self, key: UUID) -> None:
        todolist = Todolist(self.event_store.events_for(key))
        events = todolist.decide(CreateTodolist(key))
        self.event_store.save(key=key, events=events)
