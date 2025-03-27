from typing import Any

import pytest
from expression import Nothing, Ok, Result

from src.hexagon.shared.type import TodolistKey
from src.hexagon.todolist.port import TodolistSetPort
from tests.fixture import TodolistFaker
from tests.hexagon.todolist.fixture import TodolistSetForTest


class TodolistDelete:
    def __init__(self, todolist_set: TodolistSetPort) -> None:
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey) -> Result[None, None]:
        self._todolist_set.delete(todolist_key=todolist_key)
        return Ok(None)


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest) -> TodolistDelete:
    return TodolistDelete(todolist_set)


def test_delete_todolist(sut: TodolistDelete, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
    # GIVEN
    deleted_todolist = fake.a_todolist()
    todolist_set.feed(deleted_todolist)

    # WHEN
    response = sut.execute(todolist_key=deleted_todolist.to_key())

    # THEN
    assert todolist_set.by(todolist_key=deleted_todolist.to_key()) == Nothing
    assert response == Ok(None)

# def test_tell_error_when_create_existing_todolist(sut: TodolistCreate, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
#     # GIVEN
#     existing_todolist = fake.a_todolist()
#     todolist_set.feed(existing_todolist)
#
#     # WHEN
#     response = sut.execute(todolist_key=existing_todolist.to_key(), todolist_name=existing_todolist.to_name())
#
#     # THEN
#     assert response == Error(None)
