from dataclasses import dataclass, replace

from expression import Result, Error, Ok, Option, Some

from src.hexagon.shared.event import Event, TaskPostponedEvent
from src.hexagon.shared.type import TaskKey, TodolistName, TaskName, TaskExecutionDate, TaskOpen, TodolistKey


@dataclass(frozen=True ,eq=True)
class TaskSnapshot:
    key: TaskKey
    name: TaskName
    is_open: TaskOpen
    execution_date: Option[TaskExecutionDate]


@dataclass(frozen=True, eq=True)
class TodolistSnapshot:
    key: TodolistKey
    name: TodolistName
    tasks: tuple[TaskSnapshot, ...]


@dataclass(frozen=True, eq=True)
class Task:
    key: TaskKey
    name: TaskName
    is_open: TaskOpen
    execution_date: Option[TaskExecutionDate]

    def to_snapshot(self) -> TaskSnapshot:
        return TaskSnapshot(name=self.name, is_open=self.is_open, key=self.key, execution_date=self.execution_date)

    @classmethod
    def from_snapshot(cls, snapshot: TaskSnapshot) -> 'Task':
        return Task(key=snapshot.key, name=snapshot.name, is_open=snapshot.is_open,
                    execution_date=snapshot.execution_date)

    def reword(self, new_name) -> 'Task':
        return replace(self, name=new_name)

    def close_task(self) -> 'Task':
        return replace(self, is_open=TaskOpen(False))

    def postpone(self, execution_date: TaskExecutionDate):
        return replace(self, execution_date=Some(execution_date))


@dataclass(frozen=True, eq=True)
class TodolistAggregate:
    key: TodolistKey
    name: TodolistName
    tasks: tuple[Task, ...]
    events: tuple[Event, ...]

    @classmethod
    def create(cls, todolist_key: TodolistKey, todolist_name: TodolistName) -> 'TodolistAggregate':
        return TodolistAggregate(key=todolist_key, name=todolist_name, tasks=(), events=())

    @classmethod
    def from_snapshot(cls, snapshot: TodolistSnapshot) -> 'TodolistAggregate':
        return TodolistAggregate(key=snapshot.key, name=snapshot.name, tasks=(*[Task.from_snapshot(task) for task in snapshot.tasks],), events=())

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(key=self.key, name=self.name, tasks=tuple([task.to_snapshot() for task in self.tasks]))

    def open_task(self, task: Task) -> Result['TodolistAggregate', str]:
        return Ok(replace(self, tasks=self.tasks + (task,)))

    def close_task(self, key) -> Result['TodolistAggregate', str]:
        if not [task for task in self.tasks if task.key == key]:
            return Error(f"The task '{key}' does not exist")
        return Ok(replace(self, tasks=(*[task.close_task() if task.key == key else task for task in self.tasks],)))

    def reword_task(self, key: TaskKey, new_name: TaskName) -> Result['TodolistAggregate', str]:
        if not [task for task in self.tasks if task.key == key]:
            return Error(f"The task '{key}' does not exist")

        return Ok(replace(self, tasks=tuple([task.reword(new_name) if task.key == key else task for task in self.tasks],)))

    def import_tasks(self, task_snapshots: list[TaskSnapshot]) -> Result['TodolistAggregate', str]:
        return Ok(replace(self, tasks=self.tasks + (*[Task.from_snapshot(snapshot) for snapshot in task_snapshots],)))

    def postpone_task(self, key: TaskKey, execution_date: TaskExecutionDate) -> Result['TodolistAggregate', str]:
        if not [task for task in self.tasks if task.key == key]:
            return Error(f"The task '{key}' does not exist")

        tasks = tuple([task.postpone(execution_date) if task.key == key else task for task in self.tasks])
        events = self.events + (TaskPostponedEvent(task_key=key, execution_date=execution_date), )
        return Ok(replace(self, tasks=tasks, events=events))

    def uncommited_events(self) -> tuple[Event, ...]:
        return self.events