from functools import lru_cache
import os
from collections import deque


def parse(filename: str) -> list[str]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        return fd.read().splitlines()

# bfs 
def solve_part1(grid: list[str]) -> int:
    # cumulative result
    res = 0

    # setup BFS queue
    queue = deque()
    queue.append(grid[0].index("S"))
    i = 1

    while queue and i < len(grid):
        N = len(queue)
        for _ in range(N):
            pos = queue.popleft()
            if grid[i][pos] == "^":
                res += 1 # mark the split
                if pos - 1 >= 0 :
                    if (pos-1) not in queue:
                        queue.append(pos - 1)
                if pos + 1 < len(grid[0]):
                    if (pos+1) not in queue:
                        queue.append(pos + 1)
            else:
                queue.append(pos)

        # go to next row
        i += 1

    return res

# dfs 
def solve_part2(grid: list[str]) -> int:
    @lru_cache(maxsize=None)
    def f(i, pos) -> int:
        if i+1 == len(grid):
            return 1
        else:
            if grid[i][pos] == '^':
                return f(i+1, pos-1) + f(i+1, pos+1)
            else:
                return f(i+1, pos)
    return f(1, grid[0].index('S'))

if __name__ == "__main__":
    assert solve_part1(parse("example.txt")) == 21
    print(solve_part1(parse("input.txt")))
    assert solve_part2(parse("example.txt")) == 40
    print(solve_part2(parse("input.txt")))
