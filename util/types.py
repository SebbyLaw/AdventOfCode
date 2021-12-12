from typing import *

from util.parsing import Input

__all__ = (
    'SolutionFunction',
)

SolutionFunction = Callable[[Input], Any]
