"""
Singleton module utils
"""
from typing import Any, Dict


class Singleton(type):
    """
    Singleton metaclass used to create singleton classes
    """

    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
