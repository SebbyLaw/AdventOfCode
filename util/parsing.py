from __future__ import annotations

import itertools
import typing
from typing import *

import more_itertools

from util._types import Coord

__all__ = (
    'Input',
    'test',
    'Grid',
    'GridNode',
)


class Null:
    def __repr__(self) -> str:
        return 'NULL'


def test(expected: Any = Null()):
    def deco(func):
        func.__aoc_test_expected_result__ = expected
        return func
    return deco


T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @property
    def val(self) -> T:
        return self.value

    @val.setter
    def val(self, value: T):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        return self.value == other.value


class GridNode(Node[T]):
    def __init__(self, value: T, grid: Grid[T]):
        super().__init__(value)
        self._grid: Grid[T] = grid
        self.x: int = None
        self.y: int = None

    @property
    def coord(self) -> Coord:
        return self.x, self.y

    @property
    def north(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x, self.y - 1))

    @property
    def west(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x - 1, self.y))

    @property
    def east(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x + 1, self.y))

    @property
    def south(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x, self.y + 1))

    @property
    def northeast(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x + 1, self.y - 1))

    @property
    def northwest(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x - 1, self.y - 1))

    @property
    def southeast(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x + 1, self.y + 1))

    @property
    def southwest(self) -> Optional[GridNode[T]]:
        return self._grid.get((self.x - 1, self.y + 1))

    def orthogonal(self) -> Iterable[GridNode[T]]:
        return filter(None, (self.north, self.east, self.west, self.south))

    def diagonal(self) -> Iterable[GridNode[T]]:
        return filter(None, (self.northwest, self.northeast, self.southwest, self.southeast))

    def adjacent(self) -> Iterable[GridNode[T]]:
        return filter(None, (self.northwest, self.north, self.northeast, self.west, self.east, self.southwest, self.south, self.southeast))

    def __repr__(self) -> str:
        return f'<Node={self.value!r} {type(self.value)} at {self.coord}>'


class Grid(Generic[T]):
    def __init__(self, string: str, *, c: Union[Callable[[str], T], Type[T]] = str, delimiter: str = ',', newline: str = '\n'):
        r"""
        A grid.

        :param string: raw string to parse
        :param c: The type to cast to, by default this is `str` (nothing happens)
        :param delimiter: The delimiter to separate lines by, by default this is ','
        :param newline: The newline character to separate raw input into lines, by default this is '\n'
        """

        lines = string.strip().split(newline)
        self._height: int = len(lines)
        self._elements: Tuple[GridNode[T], ...] = tuple(
            GridNode(c(v), self) for v in itertools.chain.from_iterable(
                (line.split(delimiter) if delimiter not in ('', None) else iter(line))
                for line in lines
            )
        )
        self._width: int = len(self._elements) // self._height

        # link our nodes
        for i, node in enumerate(self._elements):
            node.y, node.x = divmod(i, self._width)

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def __len__(self) -> int:
        return len(self._elements)

    def __getitem__(self, coords: Coord) -> GridNode[T]:
        # x + w * y
        return self._elements[coords[0] + self._width * coords[1]]

    def get(self, coords: Coord) -> Optional[GridNode[T]]:
        x, y = coords
        if x < 0 or y < 0 or x > self._width - 1 or y > self._height - 1:
            return None
        return self[coords]

    def __iter__(self) -> Iterator[GridNode[T]]:
        return iter(self._elements)

    def rows(self) -> Iterable[Tuple[GridNode[T], ...]]:
        """Return an iterable of each row"""
        return more_itertools.grouper(self._width, self._elements)

    def columns(self) -> Iterable[Tuple[GridNode[T], ...]]:
        """Return an iterable of each column"""
        return (tuple(self[x, y] for y in range(self._height)) for x in range(self._width))

    def __str__(self) -> str:
        return '\n'.join(''.join(node.value for node in row) for row in self.rows())


class Input:
    def __init__(self, file: typing.TextIO):
        self._raw: str = file.read().strip()

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def lines(self) -> Tuple[str, ...]:
        return tuple(self._raw.splitlines(keepends=False))

    @property
    def chunks(self) -> Tuple[str, ...]:
        return tuple(self._raw.split('\n\n'))

    def __iter__(self) -> Iterator[str]:
        return iter(self.lines)

    def grid(self, *, c: Union[Callable[[str], T], Type[T]] = str, delimiter: str = ',', newline: str = '\n') -> Grid[T]:
        return Grid(self._raw, c=c, delimiter=delimiter, newline=newline)
