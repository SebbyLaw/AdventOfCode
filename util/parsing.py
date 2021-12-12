from __future__ import annotations

import itertools
import typing
from typing import *

import more_itertools

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
Number = Union[int, float]


class Node(Generic[T]):
    __slots__ = ('value', )

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
    __slots__ = ('_north', '_west', '_east', '_south', '_northeast', '_northwest', '_southeast', '_southwest', '_coord')

    def __init__(self, value: T):
        super().__init__(value)
        self._north: Optional[GridNode[T]] = None
        self._west: Optional[GridNode[T]] = None
        self._east: Optional[GridNode[T]] = None
        self._south: Optional[GridNode[T]] = None
        self._northeast: Optional[GridNode[T]] = None
        self._northwest: Optional[GridNode[T]] = None
        self._southeast: Optional[GridNode[T]] = None
        self._southwest: Optional[GridNode[T]] = None
        self._coord: Tuple[int, int] = None

    @property
    def coord(self) -> Tuple[int, int]:
        return self._coord

    @property
    def north(self) -> Optional[GridNode[T]]:
        return self._north

    @property
    def west(self) -> Optional[GridNode[T]]:
        return self._west

    @property
    def east(self) -> Optional[GridNode[T]]:
        return self._east

    @property
    def south(self) -> Optional[GridNode[T]]:
        return self._south

    @property
    def northeast(self) -> Optional[GridNode[T]]:
        return self._northeast

    @property
    def northwest(self) -> Optional[GridNode[T]]:
        return self._northwest

    @property
    def southeast(self) -> Optional[GridNode[T]]:
        return self._southeast

    def orthogonal(self) -> Iterable[GridNode[T]]:
        return filter(None, (self._north, self._east, self._west, self._south))

    def diagonal(self) -> Iterable[GridNode[T]]:
        return filter(None, (self._northwest, self._northeast, self._southwest, self._southeast))

    def adjacent(self) -> Iterable[GridNode[T]]:
        return itertools.chain(self.orthogonal(), self.diagonal())

    @property
    def southwest(self) -> Optional[GridNode[T]]:
        return self._southwest

    def __repr__(self) -> str:
        return f'<Node={self.value} {type(self.value)} at {self.coord}>'


class Grid(Generic[T]):
    def __init__(self, string: str, *, c: Union[Callable[[str], T], Type[T]] = str, delimiter: str = ',', newline: str = '\n'):
        r"""
        A grid.

        :param string: raw string to parse
        :param c: The type to cast to, by default this is `str` (nothing happens)
        :param delimiter: The delimiter to separate lines by, by default this is ','
        :param newline: The newline character to separate raw input into lines, by default this is '\n'
        """

        lines = string.split(newline)
        self._height: int = len(lines)
        self._elements: Tuple[GridNode[T], ...] = tuple(
            GridNode(c(v)) for v in itertools.chain.from_iterable(
                (line.split(delimiter) if delimiter not in ('', None) else iter(line))
                for line in lines
            )
        )
        self._width: int = len(self._elements) // self._height

        # link our nodes
        for i, node in enumerate(self._elements):
            y, x = divmod(i, self._width)
            node._coord = (x, y)
            if x > 0:
                node._west = self[x - 1, y]
            if x < self._width - 1:
                node._east = self[x + 1, y]
            if y > 0:
                node._north = self[x, y - 1]
                if node._west is not None:
                    node._northwest = self[x - 1, y - 1]
                if node._east is not None:
                    node._northeast = self[x + 1, y - 1]
            if y < self._height - 1:
                node._south = self[x, y + 1]
                if node._west is not None:
                    node._southwest = self[x - 1, y + 1]
                if node._east is not None:
                    node._southeast = self[x + 1, y + 1]

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def __len__(self) -> int:
        return len(self._elements)

    def __getitem__(self, coords: Tuple[int, int]) -> Optional[GridNode[T]]:
        # x + w * y
        try:
            return self._elements[coords[0] + self._width * coords[1]]
        except IndexError:
            return None

    def __iter__(self) -> Iterator[GridNode[T]]:
        return iter(self._elements)

    def rows(self) -> Iterable[Tuple[GridNode[T], ...]]:
        """Return an iterable of each row"""
        return more_itertools.grouper(self._width, self._elements)

    def columns(self) -> Iterable[Tuple[GridNode[T], ...]]:
        """Return an iterable of each column"""
        return (tuple(self[x, y] for x in range(self._width)) for y in range(self._height))


class Input:
    def __init__(self, file: typing.TextIO):
        self._raw: str = file.read().strip()

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def lines(self) -> Tuple[str]:
        return tuple(self._raw.splitlines(keepends=False))

    @property
    def chunks(self) -> Tuple[str]:
        return tuple(self._raw.split('\n\n'))

    def __iter__(self) -> Iterator[str]:
        return iter(self.lines)

    def grid(self, *, c: Union[Callable[[str], T], Type[T]] = str, delimiter: str = ',', newline: str = '\n') -> Grid[T]:
        return Grid(self._raw, c=c, delimiter=delimiter, newline=newline)
