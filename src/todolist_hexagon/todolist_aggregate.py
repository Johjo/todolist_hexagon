from dataclasses import dataclass
from typing import Self

from todolist_hexagon.commands import CreateTodolist, TodolistCommand, AttachTask
from todolist_hexagon.events import TodoListCreated, EventList, TaskAttached


class Todolist:
    def __init__(self, events: EventList) -> None:
        self._state = TodolistState(exist=False)
        self._evolve(events)

    def _evolve(self, events: EventList) -> None:
        if events:
            self._state = self._state.evolve()


    def decide(self, command: TodolistCommand) -> EventList:
        events : EventList = []
        match command:
            case CreateTodolist():
                if not self._state.exist:
                    events.append(TodoListCreated(todolist_key=command.key, when=command.when))

            case AttachTask(task_key=task_key, when=when):
                events.append(TaskAttached(task_key=task_key, when=when))

        return events


@dataclass(frozen=True, eq=True)
class TodolistState:
    exist: bool

    @staticmethod
    def evolve() -> 'TodolistState':
        return TodolistState(exist=True)