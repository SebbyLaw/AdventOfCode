from typing import *

__all__ = (
    'Number',
    'Coord',
)


T = TypeVar('T')
Number = Union[int, float]
Coord = Tuple[int, int]
