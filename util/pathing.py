import functools
import math
from collections import defaultdict
from typing import *

from util._types import Coord, Number
from util.parsing import Grid, GridNode

T = TypeVar('T')


class AStar(Generic[T]):
    def __init__(self, grid: Grid[T]):
        self.grid = grid

    def neighbors(self, node: GridNode[T]) -> Iterable[GridNode[T]]:
        return node.adjacent()

    @functools.lru_cache(maxsize=None)
    def _euclidean_distance(self, n1: Coord, n2: Coord) -> Number:
        return math.dist(n1, n2)

    @functools.lru_cache(maxsize=None)
    def _manhattan_distance(self, n1: Coord, n2: Coord) -> Number:
        return abs(n2[1] - n1[1]) + abs(n2[0] - n1[0])

    def traversable(self, node: GridNode[T]) -> bool:
        return True

    def h_cost(self, node: Coord, end: Coord) -> Number:
        return self._euclidean_distance(node, end)

    @functools.lru_cache(maxsize=None)
    def solve(self, start: Coord, end: Coord) -> Tuple[List[GridNode[T]], Number]:
        queue: List[Coord] = []
        done: Set[Coord] = set()
        queue.append(start)
        p_cost = defaultdict(lambda: float('inf'))
        p_cost[start] = 0
        prev = {}

        def cost(n: Coord):
            return p_cost[n] + self.h_cost(n, end)

        while True:
            curr = self.grid[min(queue, key=cost)]
            cc = curr.coord
            queue.remove(cc)
            done.add(cc)

            if cc == end:
                break

            for node in self.neighbors(curr):
                nc = node.coord
                if not self.traversable(node) or nc in done:
                    continue
                nw = cost(nc) + p_cost[cc]
                if nw < p_cost[nc] or nc not in queue:
                    p_cost[nc] = nw
                    prev[nc] = cc
                    if nc not in queue:
                        queue.append(nc)

        path = []
        step = end
        while step != start:
            path.append(self.grid[step])
            step = prev[step]
        path.reverse()
        return path, p_cost[end]


if __name__ == '__main__':
    inp = "............\n" \
          "...####..B..\n" \
          "..A...#.....\n" \
          "......#.....\n" \
          "............"

    start = (2, 2)
    end = (9, 1)

    grid = Grid(inp, delimiter='')

    class TestAS(AStar):
        def traversable(self, node: GridNode[T]) -> bool:
            return node.val != '#'

        def neighbors(self, node: GridNode[T]) -> Iterable[GridNode[T]]:
            return node.orthogonal()

        def h_cost(self, node: Coord, end: Coord) -> Number:
            return self._manhattan_distance(node, end)

    AS = TestAS(grid)
    path, cost = AS.solve(start, end)

    for n in path:
        if n.coord not in (start, end):
            n.value = 'X'

    print(grid)
