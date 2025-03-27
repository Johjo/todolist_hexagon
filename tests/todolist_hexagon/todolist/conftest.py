import pytest
from faker import Faker

from tests.fixture import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()

@pytest.fixture
def fake() -> TodolistFaker:
    fake = Faker()
    return TodolistFaker(fake)
