from collections import defaultdict
import os
import heapq
import dataclasses
from tqdm import tqdm
from functools import cache

@dataclasses.dataclass
class Point:
    x: int
    y: int


def parse(filename: str) -> list[Point]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        points = []
        for line in fd.read().splitlines():
            p = list(map(int, line.split(",")))
            points.append(Point(*p))
        return points


def area(p1: Point, p2: Point):
    x0, x1 = min(p1.x, p2.x), max(p1.x, p2.x)
    y0, y1 = min(p1.y, p2.y), max(p1.y, p2.y)
    # in the example the points are included in the rectanlge
    # so we have to sum up one to both W and H
    width = (x1 - x0) + 1
    height = (y1 - y0) + 1
    return width * height


def solve_part1(points: list[Point]) -> int:
    areas = []  # (area, p1, p2)
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            areas.append([area(points[i], points[j]), i, j])
    heapq._heapify_max(areas)
    a = heapq.heappop(areas)[0]
    return a


def solve_part2(points: list[Point]) -> int:
    # Things I've tried:
    # - Doing the line algorithm: if it crosses % 2 == 0 times we are outside, otherwise inside => gave bad result on the big input
    # - Trying to fill the rectangle causes OOM
    pass


if __name__ == "__main__":
    assert solve_part1(parse("example.txt")) == 50
    print(solve_part1(parse("input.txt")))
