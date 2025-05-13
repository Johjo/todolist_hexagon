from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

T = TypeVar('T')  # success type
E = TypeVar("E")  # error type
U = TypeVar("U")  # type for map


class Result(ABC, Generic[T, E]):
    @abstractmethod
    def is_ok(self) -> bool:
        pass

    @abstractmethod
    def is_err(self) -> bool:
        pass

    @abstractmethod
    def unwrap(self) -> T:
        pass

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> 'Result[U, E]':
        pass

    @abstractmethod
    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        pass


@dataclass(frozen=True, eq=True)
class Ok(Result[T, E]):
    value: T

    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        return f(self.value)

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        return Ok(f(self.value))


@dataclass(frozen=True, eq=True)
class Err(Result[T, E]):
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise Exception(f"Cannot unwrap Err({self.error})")

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        return Err(self.error)

    def and_then(self, f: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        return Err(self.error)
