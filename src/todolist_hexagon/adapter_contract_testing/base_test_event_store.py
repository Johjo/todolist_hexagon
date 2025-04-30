from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from todolist_hexagon.events import TaskOpened, Event, TodoListCreated, TaskDescribed, TaskClosed, TaskAttached
from todolist_hexagon.ports import AggregateEvent, EventStorePort

NOW = datetime.now()


class BaseTestEventStore(ABC):
    def test_give_nothing_when_no_events_saved(self) -> None:
        sut = self._sut()
        assert sut.events_for(key=UUID("00000000-0000-0000-0000-000000000000")) == []

    @pytest.mark.parametrize("event_name, event", [
        ["TaskOpened", TaskOpened(when=datetime.now())],
        ["TaskDescribed", TaskDescribed(title="some title", description="some description", when=datetime.now())],
        ["TaskClosed", TaskClosed(when=datetime.now())],
        ["TodoListCreated", TodoListCreated(when=datetime.now())],
        ["TaskAttached", TaskAttached(task_key=uuid4(), when=datetime.now())],
    ])
    def test_give_event_when_event_saved(self, event_name: str, event: Event) -> None:
        sut = self._sut()
        aggregate_id = UUID(int=1)
        sut.save(AggregateEvent(key=aggregate_id, events=[event]))
        assert sut.events_for(key=aggregate_id) == [event]

    def test_give_event_for_aggregate(self) -> None:
        sut = self._sut()
        aggregate_one = UUID(int=1)
        aggregate_two = UUID(int=2)
        sut.save(AggregateEvent(key=aggregate_one, events=[TodoListCreated(when=NOW)]))
        sut.save(AggregateEvent(key=aggregate_two, events=[TaskOpened(when=NOW)]))
        assert sut.events_for(key=aggregate_one) == [TodoListCreated(when=NOW)]
        assert sut.events_for(key=aggregate_two) == [TaskOpened(when=NOW)]

    def test_can_save_multiple_events_for_same_aggregate(self) -> None:
        sut = self._sut()
        aggregate_one = UUID(int=1)
        sut.save(AggregateEvent(key=aggregate_one, events=[TodoListCreated(when=NOW), TaskOpened(when=NOW)]))
        assert sut.events_for(key=aggregate_one) == [TodoListCreated(when=NOW), TaskOpened(when=NOW)]

    def test_can_save_multiple_aggregates(self) -> None:
        sut = self._sut()
        aggregate_one = UUID(int=1)
        aggregate_two = UUID(int=2)
        sut.save(AggregateEvent(key=aggregate_one, events=[TodoListCreated(when=NOW)]), AggregateEvent(key=aggregate_two, events=[TaskOpened(when=NOW)]))
        assert sut.events_for(key=aggregate_one) == [TodoListCreated(when=NOW)]
        assert sut.events_for(key=aggregate_two) == [TaskOpened(when=NOW)]

    def test_can_save_same_aggregate_without_overwriting_it(self) -> None:
        sut = self._sut()
        aggregate_one = UUID(int=1)
        sut.save(AggregateEvent(key=aggregate_one, events=[TodoListCreated(when=NOW)]))
        sut.save(AggregateEvent(key=aggregate_one, events=[TaskOpened(when=NOW)]))

        assert sut.events_for(key=aggregate_one) == [TodoListCreated(when=NOW), TaskOpened(when=NOW)]


    @abstractmethod
    def _sut(self) -> EventStorePort:
        pass
