from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass

from src.hexagon.shared.type import TaskKey, UserKey


@dataclass(frozen=True)
class Task:
    key: TaskKey

    def to_do_the_task(self):
        return DoTheTask(key=self.key)

    def to_choose_the_task(self, other_task: 'Task'):
        return ChooseTheTask(main_task_key=self.key, secondary_task_key=other_task.key)


@dataclass(frozen=True)
class NothingToDo:
    pass


@dataclass(frozen=True)
class DoTheTask:
    key: TaskKey


@dataclass(frozen=True)
class ChooseTheTask:
    main_task_key: TaskKey
    secondary_task_key: TaskKey


@dataclass(frozen=True)
class FvpSnapshot:
    task_priorities: OrderedDict[TaskKey, TaskKey]

    def to_primitive_dict(self) -> dict[TaskKey, TaskKey]:
        return {key: value for key, value in self.task_priorities.items()}

    @classmethod
    def from_primitive_dict(cls, data: dict[TaskKey, TaskKey]) -> 'FvpSnapshot':
        return FvpSnapshot(OrderedDict[TaskKey, TaskKey](data))


class FinalVersionPerfectedSession:
    def __init__(self, task_priorities: OrderedDict[TaskKey, TaskKey]):
        self.task_priorities: OrderedDict[TaskKey, TaskKey] = task_priorities

    def which_task(self, open_tasks: list[Task]) -> NothingToDo | DoTheTask | ChooseTheTask:
        ids = [task.key for task in open_tasks]
        tasks = [task for task in open_tasks if self.task_priorities.get(task.key, None) not in ids]
        match tasks:
            case [task]:
                return task.to_do_the_task()
            case [task_1, task_2, *_]:
                return task_1.to_choose_the_task(task_2)
            case _:
                return NothingToDo()

    def choose_and_ignore_task(self, id_chosen: TaskKey, id_ignored: TaskKey) -> None:
        self.task_priorities[id_ignored] = id_chosen

    def reset(self) -> None:
        self.task_priorities = OrderedDict()

    def to_snapshot(self) -> FvpSnapshot:
        return FvpSnapshot(self.task_priorities)

    @classmethod
    def from_snapshot(cls, snapshot: FvpSnapshot) -> 'FinalVersionPerfectedSession':
        return FinalVersionPerfectedSession(task_priorities=snapshot.task_priorities)

    @classmethod
    def create(cls) -> 'FinalVersionPerfectedSession':
        return FinalVersionPerfectedSession(OrderedDict())

    def cancel_priority(self, task_key: TaskKey):
        keys = list()
        for (key, value) in self.task_priorities.items():
            if value == task_key:
                keys.append(key)

        for key in keys:
            del self.task_priorities[key]


class FvpSessionSetPort(ABC):
    @abstractmethod
    def save(self, user_key: UserKey, snapshot: FvpSnapshot) -> None:
        pass

    @abstractmethod
    def by(self, user_key: UserKey) -> FvpSnapshot:
        pass
