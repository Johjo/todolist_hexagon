from dataclasses import replace
from uuid import UUID, uuid4

import pytest
from faker import Faker
from typing_extensions import Protocol

from todolist_hexagon.fvp.aggregate import Task, DoTheTask, ChooseTheTask, FvpSnapshot, NothingToDo, \
    FvpSessionSetPort
from todolist_hexagon.fvp.read.which_task import TodolistPort, WhichTaskFilter, WhichTaskQuery
from todolist_hexagon.shared.type import UserKey, TaskKey, TodolistKey
from tests.todolist_hexagon.fvp.write.fixture import FvpSessionSetForTest


class TodolistForTest(TodolistPort):
    def __init__(self) -> None:
        self._tasksByFilter: dict[tuple[UserKey, WhichTaskFilter], list[Task]] = {}

    def all_open_tasks(self, user_key: UserKey, task_filter: WhichTaskFilter) -> list[Task]:
        if (user_key, task_filter) not in self._tasksByFilter:
            raise Exception("tasks must be fed before being read")
        return self._tasksByFilter[user_key, task_filter]

    def feed(self, user_key: UserKey, task_filter: WhichTaskFilter, *tasks: Task):
        self._tasksByFilter[user_key, task_filter] = [task for task in tasks]


class QueryAdapterDependenciesPort(Protocol):
    def todolist(self) -> TodolistPort: ...

    def fvp_session_set(self) -> FvpSessionSetPort: ...


class QueryDependencies:
    def __init__(self, adapter_dependencies: QueryAdapterDependenciesPort):
        self._adapter_dependencies = adapter_dependencies

    def which_task(self):
        return WhichTaskQuery(todolist=self._adapter_dependencies.todolist(),
                              fvp_sessions_set=self._adapter_dependencies.fvp_session_set())


class AdapterDependenciesForTest:
    def __init__(self, fvp_session_set: FvpSessionSetPort | None = None, todolist_set: TodolistPort | None = None):
        self._fvp_session = fvp_session_set
        self._todolist = todolist_set

    def todolist(self) -> TodolistPort:
        if self._todolist is None:
            raise Exception("todolist not defined")
        return self._todolist

    def fvp_session_set(self) -> FvpSessionSetPort:
        if self._fvp_session is None:
            raise Exception("fvp session not defined")
        return self._fvp_session


@pytest.fixture
def sut(fvp_session_set: FvpSessionSetForTest, todolist_name: TodolistForTest):
    return QueryDependencies(
        AdapterDependenciesForTest(fvp_session_set=fvp_session_set, todolist_set=todolist_name)).which_task()



@pytest.fixture
def todolist_name():
    return TodolistForTest()


@pytest.fixture
def fvp_session_set():
    return FvpSessionSetForTest()


class FvpFaker:
    def __init__(self, fake: Faker):
        self._fake: Faker = fake

    def a_task(self, key: None | int = None) -> Task:
        if key is None:
            key = self._fake.random_int()
        return Task(key=TaskKey(UUID(int=key)))

    def a_which_task_filter(self) -> WhichTaskFilter:
        return WhichTaskFilter(todolist_key=TodolistKey(uuid4()), reference_date=self._fake.date_object(),
                               include_context=(self._fake.word(),),
                               exclude_context=(self._fake.word(),))

    def a_user_key(self) -> UserKey:
        return UserKey(self._fake.email())


@pytest.fixture
def fake() -> FvpFaker:
    return FvpFaker(Faker())


def test_which_task_without_tasks(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    task_filter = fake.a_which_task_filter()
    user_key = UserKey("the user")
    todolist_name.feed(user_key, task_filter)
    assert sut.which_task(user_key=user_key, task_filter=task_filter) == NothingToDo()


def test_which_task_with_one_task(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    # GIVEN
    user_key = UserKey("the user")
    expected_task = replace(fake.a_task(1))
    task_filter = fake.a_which_task_filter()
    todolist_name.feed(user_key, task_filter, expected_task)

    # WHEN / THEN
    assert sut.which_task(user_key=user_key, task_filter=task_filter) == DoTheTask(key=expected_task.key)


def test_which_task_with_two_tasks(sut: WhichTaskQuery, todolist_name: TodolistForTest, fake: FvpFaker):
    user_key = UserKey("the user")
    primary_task = replace(fake.a_task(1))
    secondary_task = replace(fake.a_task(2))
    task_filter = fake.a_which_task_filter()
    todolist_name.feed(user_key, task_filter, primary_task, secondary_task)

    assert sut.which_task(user_key=user_key, task_filter=task_filter) == ChooseTheTask(main_task_key=primary_task.key,
                                                                                       secondary_task_key=secondary_task.key)


def test_load_existing_session(sut: WhichTaskQuery, todolist_name: TodolistForTest,
                               fvp_session_set: FvpSessionSetForTest,
                               fake: FvpFaker):
    user_key = UserKey("the user")
    chosen_task = replace(fake.a_task(1))
    ignored_task = replace(fake.a_task(2))
    task_filter = fake.a_which_task_filter()

    fvp_session_set.feed(user_key=user_key,
                         snapshot=FvpSnapshot.from_primitive_dict({ignored_task.key: chosen_task.key}))
    todolist_name.feed(user_key, task_filter, chosen_task, ignored_task)

    assert sut.which_task(user_key=user_key, task_filter=task_filter) == DoTheTask(key=chosen_task.key)


def test_xxx(sut: WhichTaskQuery, todolist_name: TodolistForTest, fvp_session_set: FvpSessionSetForTest,
             fake: FvpFaker):
    user_one = UserKey("user_1")
    user_two = UserKey("user_2")

    task_one = replace(fake.a_task(1))
    task_two = replace(fake.a_task(2))
    task_filter = fake.a_which_task_filter()

    fvp_session_set.feed(user_key=user_one, snapshot=FvpSnapshot.from_primitive_dict({task_two.key: task_one.key}))
    fvp_session_set.feed(user_key=user_two, snapshot=FvpSnapshot.from_primitive_dict({task_one.key: task_two.key}))
    todolist_name.feed(user_one, task_filter, task_one, task_two)
    todolist_name.feed(user_two, task_filter, task_one, task_two)

    assert sut.which_task(user_key=user_one, task_filter=task_filter) == DoTheTask(key=task_one.key)
    assert sut.which_task(user_key=user_two, task_filter=task_filter) == DoTheTask(key=task_two.key)
