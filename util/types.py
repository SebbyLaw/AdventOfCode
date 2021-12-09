from typing import *

from .parsing import Input

__all__ = (
    'SolutionFunction',
)

SolutionFunction = Callable[[Input], Any]
