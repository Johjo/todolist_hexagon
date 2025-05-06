from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class CommandBase:
    when: datetime

@dataclass(frozen=True, eq=True)
class CreateTodolist(CommandBase):
    key: UUID


@dataclass(frozen=True)
class AttachTask(CommandBase):
    task_key: UUID

TodolistCommand = CreateTodolist | AttachTask


@dataclass(frozen=True)
class OpenTask(CommandBase):
    task_key: UUID
    title: str
    description: str

@dataclass(frozen=True)
class AttachSubTask(CommandBase):
    task_key: UUID


@dataclass(frozen=True)
class CloseTask(CommandBase):
    task_key: UUID


TaskCommand = OpenTask | CloseTask | AttachSubTask