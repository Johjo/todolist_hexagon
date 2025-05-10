from dataclasses import dataclass

from todolist_hexagon.commands import CreateTodolist, TodolistCommand, AttachTask
from todolist_hexagon.events import TodoListCreated, TaskAttached, Event
from todolist_hexagon.base.events import EventList


class Todolist:
    def __init__(self, events: EventList[Event]) -> None:
        self._state = TodolistState(exist=False)
        self._evolve(events)

    def _evolve(self, events: EventList[Event]) -> None:
        if events:
            self._state = self._state.evolve()

    def decide(self, command: TodolistCommand) -> EventList[Event]:
        events: EventList[Event] = []
        match command:
            case CreateTodolist():
                if not self._state.exist:
                    events.append(TodoListCreated(when=command.when))

            case AttachTask(task_key=task_key, when=when):
                events.append(TaskAttached(task_key=task_key, when=when))

        return events


@dataclass(frozen=True, eq=True)
class TodolistState:
    exist: bool

    @staticmethod
    def evolve() -> 'TodolistState':
        return TodolistState(exist=True)