from todolist_hexagon.adapter_contract_testing.base_test_event_store import BaseTestEventStore
from todolist_hexagon.events import Event
from todolist_hexagon.base.ports import EventStorePort
from todolist_hexagon.secondary.event_store_in_memory import EventStoreInMemory


class TestEventStoreInMemoryContractTesting(BaseTestEventStore):
    def _sut(self) -> EventStorePort[Event]:
        return EventStoreInMemory()




