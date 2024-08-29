"""typed_singleton package.

This package provides a decorator to create singletons.
"""

import threading
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def singleton(class_: Callable[P, T]) -> Callable[P, T]:
    """Return a singleton instance of a class.

    Args:
    ----
        class_ (Callable[P, T]): Class to be singleton.

    Returns:
    -------
        Callable[P, T]: Singleton instance of the class.

    """
    instances = {}
    lock = threading.Lock()

    @wraps(class_)
    def get_instance(*args: P.args, **kwargs: P.kwargs) -> T:
        with lock:
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
