from uuid import UUID, uuid4

import pytest

from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist
from src.hexagon.user.port import UserRepositoryPort, UserSnapshot, TodolistSnapshot


class UserRepositoryForTest(UserRepositoryPort):
    def __init__(self) -> None:
        self._snapshot: dict[UserKey, UserSnapshot] = {}

    def save(self, user: UserSnapshot) -> None:
        self._snapshot[user.key] = user

    def by_user(self, key: UserKey) -> UserSnapshot | None:
        return self._snapshot.get(key, None)


class TestCreateTodolist:
    def test_single_user_can_create_his_first_todolist(self, user_repository: UserRepositoryForTest,
                                                       sut: CreateTodolist):
        # GIVEN
        todolist_key: UUID = uuid4()
        user_key = self.any_user_key()
        todolist_name = self.any_todolist_name()

        # WHEN
        sut.execute(user_key=UserKey(user_key), todolist_key=TodolistKey(todolist_key), todolist_name=TodolistName(
            todolist_name))

        # THEN
        assert user_repository.by_user(key=UserKey(user_key)) == UserSnapshot(key=UserKey(user_key),
                                                                              todolist=(
                                                                                  TodolistSnapshot(
                                                                                      key=TodolistKey(todolist_key),
                                                                                      name=TodolistName(
                                                                                          todolist_name)),))

    def any_todolist_name(self):
        return f"my todolist{uuid4()}"

    def test_single_user_can_create_many_todolist(self, user_repository: UserRepositoryForTest, sut: CreateTodolist):
        # GIVEN
        todolist_uuid = uuid4()
        first_todolist = TodolistSnapshot(key=TodolistKey(uuid4()), name=TodolistName("my first todolist"))
        user_repository.save(UserSnapshot(key=UserKey("mail@mail.com"), todolist=(first_todolist,)))

        # WHEN
        sut.execute(user_key=UserKey("mail@mail.com"), todolist_key=TodolistKey(todolist_uuid), todolist_name=TodolistName("my second todolist"))

        # THEN
        assert user_repository.by_user(key=UserKey("mail@mail.com")) == UserSnapshot(key=UserKey("mail@mail.com"),
                                                                                     todolist=(first_todolist,
                                                                                               TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                                name=TodolistName(
                                                                                        "my second todolist"))))

    def test_many_users_can_create_todolist(self, user_repository: UserRepositoryForTest, sut: CreateTodolist):
        # GIVEN
        todolist_uuid: UUID = uuid4()
        user_key_1 = self.any_user_key()
        user_key_2 = self.any_user_key()

        # WHEN
        sut.execute(user_key=UserKey(user_key_1), todolist_key=TodolistKey(todolist_uuid), todolist_name=TodolistName("my todolist for user 1"))
        sut.execute(user_key=UserKey(user_key_2), todolist_key=TodolistKey(todolist_uuid), todolist_name=TodolistName("my todolist for user 2"))

        # THEN
        assert user_repository.by_user(key=UserKey(user_key_1)) == UserSnapshot(key=UserKey(user_key_1),
                                                                                todolist=(
                                                                                TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                 name=TodolistName("my todolist for user 1")),))
        assert user_repository.by_user(key=UserKey(user_key_2)) == UserSnapshot(key=UserKey(user_key_2),
                                                                                todolist=(
                                                                                TodolistSnapshot(key=TodolistKey(todolist_uuid),
                                                                                                 name=TodolistName("my todolist for user 2")),))

    @pytest.fixture
    def user_repository(self) -> UserRepositoryForTest:
        return UserRepositoryForTest()

    @pytest.fixture
    def sut(self, user_repository: UserRepositoryForTest) -> CreateTodolist:
        return CreateTodolist(user_repository=user_repository)

    @staticmethod
    def any_user_key():
        return f'mail{uuid4()}@mail.com'

