"""Common types.
"""
from typing import Any, Callable, Coroutine, Iterable, TypeVar

T = TypeVar("T")
TIterable = TypeVar("TIterable", bound=Iterable)

TClass = TypeVar("TClass", bound=type)
TDecoratedCallable = TypeVar("TDecoratedCallable", bound=Callable[..., Any])

Timestamp = float
Delta = float

CashOperator = str
"""
Special string literal starts with dollar sign `$` which holds a special
meaning to the acceptor logic.
"""

AnyCoro = Coroutine[Any, Any, Any]
