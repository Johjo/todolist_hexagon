from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class CreateTodolist:
    key: UUID


@dataclass
class AttachTask:
    task_key: UUID

TodolistCommand = CreateTodolist | AttachTask
