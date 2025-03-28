from dataclasses import dataclass, replace
from datetime import datetime, date
from typing import cast
from uuid import UUID, uuid4

from expression import Option, Nothing, Some
from faker import Faker

from todolist_hexagon.shared.type import TaskKey, TaskName, TodolistName, TaskOpen, TaskExecutionDate, TodolistKey
from todolist_hexagon.todolist.aggregate import TaskSnapshot, TodolistSnapshot


def a_task_key(index: TaskKey | UUID | int | None = None) -> TaskKey:
    if isinstance(index, int):
        return TaskKey(UUID(int=index))
    if isinstance(index, UUID):
        return TaskKey(index)
    return TaskKey(uuid4())


@dataclass(frozen=True)
class TaskBuilder:
    key: TaskKey | UUID | None = None
    name: TaskName | str | None = None
    is_open: TaskOpen | bool | None= None
    execution_date: Option[TaskExecutionDate | date] | TaskExecutionDate | date | None = None

    def having(self, **kwargs) -> 'TaskBuilder':
        return replace(self, **kwargs)

    def to_snapshot(self) -> TaskSnapshot:
        return TaskSnapshot(key=self.to_key(), name=self.to_name(), is_open=self.to_open(), execution_date=self.to_execution_date())

    def to_key(self) -> TaskKey:
        if self.key is None:
            raise Exception("task.key must be set")
        return TaskKey(self.key)

    def to_name(self) -> TaskName:
        if self.name is None:
            raise Exception("task.name must be set")
        return TaskName(self.name)

    def to_open(self) -> TaskOpen:
        if self.is_open is None:
            raise Exception("task.is_open must be set")
        return TaskOpen(self.is_open)

    def to_execution_date(self) -> Option[TaskExecutionDate] :
        if self.execution_date is None:
            raise Exception("task.execution_date must be set")
        if self.execution_date == Nothing:
            return Nothing
        if isinstance(self.execution_date, datetime):
            return Some(TaskExecutionDate(self.execution_date))
        if isinstance(self.execution_date, Option):
            return cast(Option[TaskExecutionDate], self.execution_date)
        return Some(TaskExecutionDate(self.execution_date))


@dataclass(frozen=True)
class TodolistBuilder:
    key: TodolistKey
    name: TodolistName = TodolistName("undefined")
    tasks: list[TaskBuilder] | None= None

    def having(self, **kwargs) -> 'TodolistBuilder':
        return replace(self, **kwargs)

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(key=self.to_key(), name=self.to_name(), tasks=tuple(task.to_snapshot() for task in self.to_tasks()))

    def to_tasks(self) -> list[TaskBuilder]:
        if self.tasks is None:
            raise Exception("todolist.tasks must be set")
        return self.tasks

    def to_name(self) -> TodolistName:
        if self.name == "undefined":
            raise Exception("todolist.name must be set")
        return TodolistName(self.name)

    def to_key(self) -> TodolistKey:
        return self.key


@dataclass(frozen=True)
class TaskFilterBuilder:
    todolist_name: str | None = None

    def to_todolist_name(self):
        if self.todolist_name is None:
            raise Exception("feed todolist name before getting filter")
        return TodolistName(self.todolist_name)


class TodolistFaker:
    def __init__(self, fake: Faker):
        self.fake = fake

    def a_task(self, key: None | int | UUID = None) -> TaskBuilder:
        return TaskBuilder(key=self.task_key(key), name=self.task_name(), is_open=True, execution_date=Nothing)

    def a_closed_task(self, key: None | int | UUID = None) -> TaskBuilder:
        return self.a_task(key).having(is_open=False)

    def a_todolist(self, name: TodolistName | str | None = None) -> TodolistBuilder:
        if name is None:
            name = self.fake.word()
        return TodolistBuilder(key= TodolistKey(uuid4()), name=TodolistName(name), tasks=[])

    @staticmethod
    def task_key(key: None | int | UUID | TaskKey = None) -> TaskKey:
        if key is None:
            return TaskKey(uuid4())
        if isinstance(key, int):
            return TaskKey(UUID(int=key))
        return TaskKey(key)

    def task_name(self) -> TaskName:
        return TaskName(self.fake.sentence())

    def a_task_filter(self, todolist_name: str) -> TaskFilterBuilder:
        return TaskFilterBuilder(todolist_name=todolist_name)



    def a_date(self, before: date | None = None, after: date | None = None) -> date:
        if not before:
            before = date(2030, 10, 17)
        if not after:
            after = date(1930, 10, 17)
        return cast(date, self.fake.date_between(start_date=after, end_date=before))

    def many_task(self, number_of_task: int) -> list[TaskBuilder]:
        return [self.a_task() for _ in range(number_of_task)]

    def a_user_key(self) -> str:
        return self.fake.email()

    def a_datetime(self) -> datetime:
        return self.fake.date_time()
