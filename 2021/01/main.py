from util.old import read

def sol1(inp):
    x = 0
    for i, n in enumerate(inp):
        if n > inp[i - 1]:
            x += 1

    return x

def sol2(inp):
    windows = []
    for i, n in enumerate(inp):
        if i == len(inp) - 2:
            break

        windows.append(n + inp[i + 1] + inp[i + 2])

    return sol1(windows)


if __name__ == '__main__':
    print(sol1(read()))
    print(sol2(read()))
