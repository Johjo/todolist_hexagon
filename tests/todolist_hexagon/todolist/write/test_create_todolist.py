import pytest
from expression import Ok, Error

from todolist_hexagon.todolist.write.create_todolist import TodolistCreate
from src.use_case_dependencies import UseCaseDependencies
from tests.fixture import TodolistFaker
from tests.todolist_hexagon.todolist.fixture import TodolistSetForTest
from tests.todolist_hexagon.adapter_dependencies_for_test import AdapterDependenciesForTest


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()


@pytest.fixture
def sut(todolist_set: TodolistSetForTest) -> TodolistCreate:
    return UseCaseDependencies(AdapterDependenciesForTest(todolist_set)).create_todolist()


def test_create_todolist(sut: TodolistCreate, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
    # GIVEN
    expected_todolist = fake.a_todolist()
    todolist_set.feed_nothing(todolist_key=expected_todolist.to_key())

    #WHEN
    response = sut.execute(todolist_key=expected_todolist.to_key(), todolist_name=expected_todolist.to_name())

    # THEN
    assert todolist_set.by(todolist_key=expected_todolist.to_key()).value == expected_todolist.to_snapshot()
    assert response == Ok(None)


def test_tell_error_when_create_existing_todolist(sut: TodolistCreate, todolist_set: TodolistSetForTest, fake: TodolistFaker) -> None:
    # GIVEN
    existing_todolist = fake.a_todolist()
    todolist_set.feed(existing_todolist)

    # WHEN
    response = sut.execute(todolist_key=existing_todolist.to_key(), todolist_name=existing_todolist.to_name())

    # THEN
    assert response == Error(None)
