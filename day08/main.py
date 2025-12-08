from collections import Counter
import os
import math
import dataclasses
import heapq


@dataclasses.dataclass
class Point3D:
    x: int
    y: int
    z: int


def parse(filename: str) -> list[Point3D]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = fd.read().splitlines()
        return [Point3D(*map(int, line.split(","))) for line in lines]


def euclidean_dist(p1: Point3D, p2: Point3D) -> float:
    """https://en.wikipedia.org/wiki/Euclidean_distance"""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)


def solve_part1(points: list[Point3D], steps: int) -> int:
    # compute distances among all points
    heap = []
    for i in range(len(points)):
        for j in range(0, i):
            d = euclidean_dist(points[i], points[j])
            heap.append((d, i, j))

    # build heap, in place, linear O(n)
    heapq.heapify(heap)

    # "coloring" to track groups
    C = list(range(-1, -len(points) - 1, -1))
    current_color = 1
    for _ in range(steps):
        _, i, j = heapq.heappop(heap)
        if C[i] < 0 and C[j] < 0:
            # both points do not belong to any group
            # form a new group
            C[i], C[j] = current_color, current_color
            current_color += 1
        elif C[i] < 0:
            # merge point i to point j group
            C[i] = C[j]
        elif C[j] < 0:
            # merge point j to point i group
            C[j] = C[i]
        else:
            # merge two groups
            ci, cj = C[i], C[j]
            color = min(ci, cj)
            for k in range(len(points)):
                if C[k] == ci or C[k] == cj:
                    C[k] = color
    
    # final ans: multiply together the sizes of the three largest circuits
    res = 1
    for _, count in Counter(C).most_common(3):
        res *= count
    return res


def solve_part2(points: list[Point3D]) -> int:
    # compute distances among all points
    heap = []
    for i in range(len(points)):
        for j in range(0, i):
            d = euclidean_dist(points[i], points[j])
            heap.append((d, i, j))

    # build heap, in place, linear O(n)
    heapq.heapify(heap)

    # "coloring" to track groups
    C = list(range(-1, -len(points) - 1, -1))
    current_color = 1
    while len(set(C)) != 1:
        _, i, j = heapq.heappop(heap)
        if C[i] < 0 and C[j] < 0:
            # both points do not belong to any group
            # form a new group
            C[i], C[j] = current_color, current_color
            current_color += 1
        elif C[i] < 0:
            # merge point i to point j group
            C[i] = C[j]
        elif C[j] < 0:
            # merge point j to point i group
            C[j] = C[i]
        else:
            # merge two groups
            ci, cj = C[i], C[j]
            color = min(ci, cj)
            for k in range(len(points)):
                if C[k] == ci or C[k] == cj:
                    C[k] = color

        # ans will be P1.x * P2.x
        res = points[i].x * points[j].x
    
    return res



if __name__ == "__main__":
    assert solve_part1(parse("example.txt"), steps=10) == 40
    print(solve_part1(parse("input.txt"), steps=1000))
    assert solve_part2(parse("example.txt")) == 25272
    print(solve_part2(parse("input.txt")))
