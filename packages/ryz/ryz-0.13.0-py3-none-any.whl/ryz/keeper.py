"""
Smart data containers.
"""

from typing import Generic, TypeVar

from ryz.core import Err, Ok, Res, ecode
from ryz.range import Range

T = TypeVar("T")

class Keeper(Generic[T]):
    """
    Manages acquisition strategy for some set of values of the same type.

    In default implementations is supposed to give unique value each new
    request, and to avoid overflows, supports freeing methods, so previously
    obtained values can be returned to the keeper.
    """
    def recv(self) -> Res[T]:
        """
        Receive a new unique val from the keeper.
        """
        raise NotImplementedError

    def free(self, val: T) -> Res[None]:
        """
        Frees val so it's again available in the container.
        """
        raise NotImplementedError

class IntKeeper(Keeper[int]):
    """
    Holds available ints for things like consequent ids.
    """
    def __init__(self, range_: Range[int] = Range(0, 1_000_000)) -> None:
        super().__init__()
        self._range = range_
        self._given: set[int] = set()

    def recv(self) -> Res[int]:
        for possible in self._range.get_python_range():
            if possible not in self._given:
                self._given.add(possible)
                return Ok(possible)
        return Err("no available values")

    def free(self, val: int) -> Res[None]:
        if val not in self._given:
            return Err(f"val {val}", ecode.NotFound)
        self._given.remove(val)
        return Ok(None)
