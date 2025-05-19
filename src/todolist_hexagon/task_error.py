from dataclasses import dataclass


@dataclass(frozen=True)
class TaskNotFound:
    pass


@dataclass(frozen=True)
class TaskAlreadyClosed:
    pass


@dataclass(frozen=True)
class TaskHavingOpenedSubTask:
    pass


TaskError = TaskNotFound | TaskAlreadyClosed | TaskHavingOpenedSubTask
