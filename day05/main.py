import os
import tqdm
import math
from collections import deque


def parse(filename: str) -> tuple[list[range], list[int]]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = [line.strip() for line in fd.readlines()]
        fids, ids = lines[: lines.index("")], lines[lines.index("") + 1 :]
        freshIds: list[range] = []
        for x in fids:
            b, e = x.split("-")
            freshIds.append(range(int(b), int(e) + 1))
        ids = list(map(int, ids))
        return freshIds, ids


def solve_part1(freshIds: list[range], ids: list[int]) -> int:
    res = 0
    for x in ids:
        for fid_range in freshIds:
            if x in fid_range:
                res += 1
                break
    return res


def solve_part2(freshIds: list[range], ids: list[int]) -> int:
    res: int = 0

    events: list[tuple[int, int]] = []
    for xrange in freshIds:
        events.append((xrange[0], 1))
        events.append((xrange[-1] + 1, -1))
    events = sorted(events, key=lambda x: x[0])  # by time

    pts = deque()
    for t, d in events:
        if d == 1:
            pts.append(t)
        else:
            x = pts.popleft()
            if len(pts) == 0:
                res += t - x
            else:
                res += pts[0] - x
    return res


if __name__ == "__main__":
    assert solve_part1(*parse("example.txt")) == 3
    print(solve_part1(*parse("input.txt")))
    assert solve_part2(*parse("example.txt")) == 14
    print(solve_part2(*parse("input.txt")))
