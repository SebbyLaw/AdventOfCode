from __future__ import annotations

from typing import *

from util.parsing import Node

__all__ = (
    'Graph',
    'GraphNode',
)


T = TypeVar('T')
Number = Union[int, float]


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
        if node.value not in self._weights:
            self._weights[node.value] = weight

    @property
    def smallest(self) -> GraphNode[T]:
        return self._graph[min(self._weights, key=self._weights.get)]

    @property
    def largest(self) -> GraphNode[T]:
        return self._graph[max(self._weights, key=self._weights.get)]

    def __repr__(self):
        return f'<Node ({self.value})>'


class Graph(Generic[T]):
    def __init__(self):
        self._elements: Dict[str, GraphNode[T]] = {}

    def add_node(self, value: T) -> GraphNode[T]:
        if value in self._elements:
            return self._elements[value]
        else:
            node = GraphNode(value, self)
            self._elements[value] = node
            return node

    def __len__(self) -> int:
        return len(self._elements)

    def __iter__(self) -> Iterator[GraphNode[T]]:
        return iter(self._elements.values())

    def __getitem__(self, item) -> Optional[GraphNode[T]]:
        return self._elements[item]

    def dijkstra(self, start: GraphNode[T], end: GraphNode[T]) -> Tuple[List[GraphNode[T]], Number]:
        """Returns the shortest path from a starting node and its cost."""
        unvisited = set(self._elements)
        dist = {n: float('inf') for n in self._elements}
        dist[start.value] = 0
        prev = {}
        while True:
            curr = self._elements[min(unvisited, key=dist.get)]
            if curr == end:
                break
            unvisited.remove(curr.value)
            for node, weight in curr.neighbors(True):
                nw = weight + dist[curr.value]
                if nw < dist[node.value]:
                    dist[node.value] = nw
                    prev[node.value] = curr.value

        path = []
        step = end.value
        while True:
            path.append(self._elements[step])
            try:
                step = prev[step]
            except KeyError:
                path.reverse()
                return path, dist[end.value]


if __name__ == '__main__':
    from termcolor import cprint

    # Test dijkstra from 2019 day 6 example problem
    inp = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
    graph: Graph[str] = Graph()
    for line in inp.splitlines():
        a, b = line.split(')')
        a = graph.add_node(a)
        b = graph.add_node(b)
        a.add_neighbor(b)
        b.add_neighbor(a)

    sol, cost = graph.dijkstra(graph['YOU'], graph['SAN'])
    passed = cost - 2 == 4
    cprint(f'Graph.dijkstra(): {"Pass" if passed else "Fail"}', 'green' if passed else 'red')

