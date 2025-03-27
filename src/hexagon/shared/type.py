from datetime import date
from typing import NewType
from uuid import UUID

UserKey = NewType('UserKey', str)

TodolistKey = NewType('TodolistKey', UUID)
TodolistName = NewType('TodolistName', str)
TodolistContext = NewType('TodolistContext', str)
TodolistContextCount = NewType('TodolistContextCount', int)

TaskKey = NewType('TaskKey', UUID)
TaskName = NewType('TaskName', str)
TaskOpen = NewType('TaskOpen', bool)
TaskExecutionDate = NewType('TaskExecutionDate', date)

