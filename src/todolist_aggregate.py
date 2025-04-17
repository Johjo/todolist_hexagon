from src.commands import CreateTodolist
from src.events import TodoListCreated, EventList

Command = CreateTodolist

class Todolist:
    def __init__(self, events: EventList) -> None:
        self._exist : bool = False
        self._evolve(events)

    def _evolve(self, events: EventList) -> None:
        self._exist = events

    def decide(self, command: Command) -> EventList:
        events = []
        if not self._exist:
            events = [TodoListCreated(command.key)]
        return events
