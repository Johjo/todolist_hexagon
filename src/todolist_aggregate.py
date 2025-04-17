from dataclasses import dataclass

from src.commands import CreateTodolist
from src.events import TodoListCreated, EventList

Command = CreateTodolist

class Todolist:
    def __init__(self, events: EventList) -> None:
        self._state = TodolistState(exist=False)
        self._evolve(events)

    def _evolve(self, events: EventList) -> None:
        self._state = TodolistState(exist=len(events) > 0)


    def decide(self, command: Command) -> EventList:
        events = []
        if not self._state.exist:
            events = [TodoListCreated(command.key)]
        return events


@dataclass(frozen=True, eq=True)
class TodolistState:
    exist: bool