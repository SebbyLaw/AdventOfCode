from util import *


@test(40)
def p1(inp: Input):
    grid = inp.grid(c=int, delimiter='')
    graph = Graph()
    for i in grid:
        node = graph.add_node(i.coord)
        for ne in i.orthogonal():
            other = graph.add_node(ne.coord)
            node.add_neighbor(other, weight=ne.val)
            other.add_neighbor(node, weight=i.val)

    p, cost = graph.dijkstra((0, 0), (grid.width - 1, grid.height - 1))
    return cost


def inc(d: int, n: int) -> int:
    ans = d + n
    if ans > 9:
        return ans - 9
    return ans


# this is slow
@test(315)
def p2(inp: Input):
    # do something cursed to get the joined grid
    nine: List[Grid[int]] = []
    for i in range(0, 9):
        g = inp.grid(c=int, delimiter='')
        for e in g:
            e.value = inc(e.value, i)
        nine.append(g)
    height = nine[0].height
    com: List[List[str]] = []
    for _ in range(5):
        com.append([''] * height)
    for c in range(5):
        for r in range(5):
            grid = nine[c + r]
            for i, row in enumerate(grid.rows()):
                com[c][i] += ''.join(str(el.value) for el in row)
    string = '\n'.join('\n'.join(row) for row in (rows for rows in com))

    # now just dijkstra again
    grid = Grid(string, c=int, delimiter='')
    graph = Graph()
    for i in grid:
        node = graph.add_node(i.coord)
        for ne in i.orthogonal():
            other = graph.add_node(ne.coord)
            node.add_neighbor(other, weight=ne.val)
            other.add_neighbor(node, weight=i.val)

    p, cost = graph.dijkstra((0, 0), (grid.width - 1, grid.height - 1))
    return cost
