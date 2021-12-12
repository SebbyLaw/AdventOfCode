from util import *


def small_only_once(l):
    return len([i for i in l if len(i) == 1 and i.islower()]) <= 1


@test(10)
def p1(inp: Input):
    paths = []
    graph: Graph[str] = Graph()
    for i in inp:
        for n in i.split('-'):
            graph.add_node(n)

    for i in inp:
        a, b = i.split('-')
        a, b = graph[a], graph[b]
        a.add_neighbor(b)
        b.add_neighbor(a)

    def build(curr: str, p: list):
        p.append(curr)
        if curr == 'end':
            paths.append(p)
            return

        for nxt in graph[curr].neighbors():
            if nxt.val == 'start':
                continue
            if nxt.val.islower():
                if nxt.val in p:
                    continue
            build(nxt.val, p.copy())

    build('start', [])
    return len(paths)


@test(36)
def p2(inp: Input):
    paths = []
    graph: Graph[str] = Graph()
    for i in inp:
        for n in i.split('-'):
            graph.add_node(n)

    for i in inp:
        a, b = i.split('-')
        a, b = graph[a], graph[b]
        a.add_neighbor(b)
        b.add_neighbor(a)

    def visited_small_twice(p):
        for n in p:
            if n.islower() and p.count(n) == 2:
                return True
        return False

    def build(curr: str, p: list):
        p.append(curr)
        if curr == 'end':
            paths.append(p)
            return

        for nxt in graph[curr].neighbors():
            if nxt.val == 'start':
                continue
            if nxt.val.islower():
                vst = visited_small_twice(p)
                if vst and nxt.val in p:
                    continue

            build(nxt.val, p.copy())

    build('start', [])
    return len(paths)
