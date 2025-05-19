from dataclasses import dataclass, field, replace
from datetime import datetime
from typing import assert_never, cast
from uuid import UUID

from todolist_hexagon.base.events import EventList
from todolist_hexagon.base.ports import EventStorePort
from todolist_hexagon.commands import TaskCommand, OpenTask, CloseTask, AttachSubTask, DescribeTask
from todolist_hexagon.events import TaskEvent, TaskDescribed, TaskClosed, TaskOpened, SubTaskAttached, Event
from todolist_hexagon.result import Result, Ok, Err
from todolist_hexagon.task_error import TaskError, TaskNotFound, TaskAlreadyClosed, TaskHavingOpenedSubTask


@dataclass(frozen=True, eq=True)
class TaskState:
    exist: bool = False
    is_closed: bool = False
    at_least_one_sub_task_is_opened: bool = False
    sub_tasks_key: list[UUID] = field(default_factory=list)

    def evolve(self, event: TaskEvent) -> 'TaskState':
        match event:
            case TaskDescribed():
                pass
            case TaskClosed():
                return replace(self, is_closed=True, exist=True)

            case TaskOpened():
                pass
            case SubTaskAttached():
                return replace(self, at_least_one_sub_task_is_opened=True, sub_tasks_key=self.sub_tasks_key + [event.task_key])

            case _:
                assert_never(event)

        return TaskState(exist=True)


def is_sub_task_opened(history: EventList[TaskEvent]) -> bool:
    is_opened = False
    for event in history:
        match event:
            case TaskOpened():
                is_opened = True
            case TaskClosed():
                is_opened = False
            case TaskDescribed():
                pass
            case SubTaskAttached():
                pass
            case _:
                assert_never(event)
    return is_opened


class Task:
    def __init__(self, task_key: UUID, event_store: EventStorePort[Event]) -> None:
        self._event_store = event_store
        self.state = TaskState()
        for event in event_store.events_for(key=task_key):
            self.state = self.state.evolve(cast(TaskEvent, event))



    def decide(self, command: TaskCommand) -> Result[EventList[Event], TaskError]:
        match command:
            case OpenTask(title=title, description=description, when=when):
                return Ok([TaskDescribed(title=title, description=description, when=when), TaskOpened(when=when)])

            case CloseTask(when=when):
                return self._close_task(when)

            case AttachSubTask(task_key=task_key, when=when):
                return Ok([SubTaskAttached(task_key=task_key, when=when)])

            case DescribeTask(title=title, description=description, when=when):
                if self.state.exist:
                    return Ok([TaskDescribed(title=title, description=description, when=when)])
                return Err(TaskNotFound())

            case _:
                raise NotImplementedError(command)

    def _close_task(self, when: datetime) -> Result[EventList[Event], TaskError]:
        if not self.state.exist:
            return Err(TaskNotFound())
        if self.state.is_closed:
            return Err(TaskAlreadyClosed())
        if self.state.sub_tasks_key:
            at_least_one_sub_task_is_opened = False
            for sub_task_key in self.state.sub_tasks_key:
                events_for = cast(EventList[TaskEvent], self._event_store.events_for(sub_task_key))
                if is_sub_task_opened(events_for):
                    at_least_one_sub_task_is_opened = True
            if at_least_one_sub_task_is_opened:
                return Err(TaskHavingOpenedSubTask())
        return Ok([TaskClosed(when=when)])
