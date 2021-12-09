import collections
import math
from typing import List, Tuple
import functools

from util import *


@test(15)
def p1(inp: Input):
    total = 0
    lines = list(list(map(int, line)) for line in inp)
    for i, line in enumerate(lines):
        for j, n in enumerate(line):
            if (j == 0 or n < line[j - 1]) and (j == len(line) - 1 or n < line[j + 1]) and (i == 0 or n < lines[i - 1][j]) and (i == len(lines) - 1 or n < lines[i + 1][j]):
                total += n + 1

    return total


@test(1134)
def p2_old(inp: Input):
    basins: List[List[Tuple[int, int]]] = []

    m = tuple((int(i) for i in line) for line in inp)

    @functools.lru_cache(maxsize=None)
    def neighbors(x, y):
        return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)

    for x, line in enumerate(m):
        for y, c in enumerate(line):
            if c != 9:
                for basin in basins:
                    if any(n in basin for n in neighbors(x, y)):
                        basin.append((x, y))
                        break
                else:
                    basins.append([(x, y)])

    def is_same_basin(basin_1, basin_2):
        for n in basin_1:
            for c in basin_2:
                if c in neighbors(*n):
                    return True
        return False

    # merge connected basins
    counted = set()
    keep = []
    for i, basin in enumerate(basins[:-1]):
        if i in counted:
            continue
        else:
            basin = set(basin)
            keep.append(basin)
            for j, other in enumerate(basins[i:], start=i):
                if is_same_basin(basin, other):
                    counted.add(j)
                    basin.update(other)

    keep = reversed(sorted(map(len, keep)))
    return next(keep) * next(keep) * next(keep)


@test(1134)
def p2(inp: Input):
    grid: Grid[int] = inp.grid(c=int, delimiter='')
    basins = {}

    def search(node: Node[int], v):
        if node.coord in basins or node.val == 9:
            return
        basins[node.coord] = v
        for q in node.orthogonal():
            search(q, v)

    for i, n in enumerate(grid):
        search(n, i)  # type: ignore # enumerate isn't typed? idk

    return math.prod(c for _, c in collections.Counter(basins.values()).most_common(3))
