from __future__ import annotations

import queue
from typing import *

from util._types import Number
from util.errors import NoPathPossible
from util.parsing import Node

__all__ = (
    'Graph',
    'GraphNode',
)


T = TypeVar('T')


class GraphNode(Node[T]):
    __slots__ = ('_weights', '_graph')

    def __init__(self, value: T, graph: Graph[T]):
        super().__init__(value)
        self._graph = graph
        self._weights: Dict[T, Number] = {}

    def neighbors(self, with_weights: bool = False) -> Union[Iterable[GraphNode[T]], Iterable[Tuple[GraphNode[T], Number]]]:
        if with_weights:
            return ((self._graph[n], v) for n, v in self._weights.items())
        return (self._graph[n] for n in self._weights)

    def add_neighbor(self, node: GraphNode[T], weight: Number = 1) -> None:
        if self == node:
            return
        if node.value not in self._weights:
            self._weights[node.value] = weight

    @property
    def smallest(self) -> GraphNode[T]:
        return self._graph[min(self._weights, key=self._weights.get)]

    @property
    def largest(self) -> GraphNode[T]:
        return self._graph[max(self._weights, key=self._weights.get)]

    def __repr__(self):
        return f'<Node ({self.value!r})>'


K = TypeVar('K')


class Graph(Generic[T]):
    def __init__(self):
        self._elements: Dict[K, GraphNode[T]] = {}

    def add_node(self, value: K) -> GraphNode[T]:
        if value in self._elements:
            return self._elements[value]
        else:
            node = GraphNode(value, self)
            self._elements[value] = node
            return node

    def add_nodes(self, *values: K, weight: Number = 1) -> Tuple[GraphNode[T], ...]:
        nodes = tuple((v not in self._elements) and GraphNode(v, self) or self._elements[v] for v in values)
        for node in nodes:
            self._elements[node.value] = node
            for other in nodes:
                node.add_neighbor(other, weight=weight)
        return nodes

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator[GraphNode[T]]:
        return iter(self._elements.values())

    def __getitem__(self, item) -> Optional[GraphNode[T]]:
        return self._elements[item]

    def dijkstra(self, start: T, end: T) -> Tuple[List[GraphNode[T]], Number]:
        """Returns the shortest path from a starting node and its cost."""
        dist = {start: 0}
        prev = {}

        unvisited = queue.PriorityQueue()
        for e, v in self._elements.items():
            if e != start:
                dist[e] = float('inf')

            unvisited.put((dist[e], e))

        while True:
            try:
                curr = self._elements[unvisited.get(block=False)[1]]
            except (ValueError, queue.Empty):
                raise NoPathPossible() from None
            cv = curr.value
            if cv == end:
                break
            for node, weight in curr.neighbors(True):
                nv = node.value
                nw = weight + dist[cv]
                if nw < dist[nv]:
                    dist[nv] = nw
                    unvisited.put((dist[nv], nv))
                    prev[nv] = cv

        path = [self._elements[start]]
        step = end
        while step != start:
            path.append(self._elements[step])
            step = prev[step]
        path.reverse()
        return path, dist[end]


if __name__ == '__main__':
    from termcolor import cprint

    # Test dijkstra from 2019 day 6 example problem
    inp = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
    graph: Graph[str] = Graph()
    for line in inp.splitlines():
        a, b = line.split(')')
        a, b = graph.add_nodes(a, b)

    sol, cost = graph.dijkstra('YOU', 'SAN')
    passed = cost - 2 == 4
    cprint(f'Graph.dijkstra(): {"Pass" if passed else "Fail"}', 'green' if passed else 'red')

