from uuid import UUID

from todolist_hexagon.base.ports import EventStorePort, AggregateEvent
from todolist_hexagon.events import Event
from todolist_hexagon.base.events import EventList


class EventStoreInMemory(EventStorePort[Event]):
    def __init__(self) -> None:
        self.events : dict[UUID, EventList[Event]] = {}

    def save(self, *aggregate_events: AggregateEvent[Event]) -> None:
        for truc in aggregate_events:
            self.events.setdefault(truc.key, [])
            self.events[truc.key].extend(truc.events)

    def events_for(self, key: UUID) -> EventList[Event]:
        return self.events.get(key, [])
