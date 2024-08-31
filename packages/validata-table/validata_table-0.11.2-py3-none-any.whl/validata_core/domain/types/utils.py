from typing import Optional, Tuple, TypeVar

from .error import Error

# Handling Errors as values
T = TypeVar("T")
E = TypeVar("E", bound=Error)

Res = Tuple[T, Optional[E]]
