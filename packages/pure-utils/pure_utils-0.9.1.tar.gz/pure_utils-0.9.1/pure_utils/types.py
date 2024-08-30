"""Helper module with common types.

Available common types:

.. code-block:: python

    T = TypeVar("T")
    P = ParamSpec("P")
    KeysT: TypeAlias = Sequence[T] | KeysView[T]
    ExceptionT = Type[BaseException]
    CallableAnyT: TypeAlias = Callable[[Any], Any]
"""

from typing import (
    Any,
    Callable,
    KeysView,
    ParamSpec,
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
)

T = TypeVar("T")
P = ParamSpec("P")
KeysT: TypeAlias = Sequence[T] | KeysView[T]
ExceptionT = Type[BaseException]
CallableAnyT: TypeAlias = Callable[[Any], Any]
