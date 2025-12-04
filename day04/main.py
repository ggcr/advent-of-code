import os
from copy import deepcopy


def parse(filename: str) -> list[list[str]]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        grid = []
        for line in fd.readlines():
            grid.append(list(line.strip()))
        return grid


def solve_part1(grid: list[list[str]]) -> tuple[list[list[str]], int]:
    res = deepcopy(grid)

    # cache the coords for easy out of bounds
    coordset = {}
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            coordset[(i, j)] = True

    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != "@":
                continue

            tl = (i - 1, j - 1)
            t = (i - 1, j)
            tr = (i - 1, j + 1)
            r = (i, j + 1)
            br = (i + 1, j + 1)
            b = (i + 1, j)
            bl = (i + 1, j - 1)
            l = (i, j - 1)

            papers = 0
            for idx in [tl, t, tr, r, br, b, bl, l]:
                if idx not in coordset:
                    continue
                if grid[idx[0]][idx[1]] == "@":
                    papers += 1

            if papers < 4:
                res[i][j] = "."
                count += 1

    return (res, count)


def solve_part2(grid: list[list[str]]) -> int:
    total = 0
    while True:
        grid, count = solve_part1(grid)
        total += count
        if count == 0:
            break
    return total


if __name__ == "__main__":
    assert solve_part1(parse("example.txt"))[-1] == 13
    print(solve_part1(parse("input.txt"))[-1])
    assert solve_part2(parse("example.txt")) == 43
    print(solve_part2(parse("input.txt")))
