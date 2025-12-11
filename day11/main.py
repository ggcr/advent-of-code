import os
from dataclasses import dataclass
from functools import cache


class Node:
    def __init__(self, value: str):
        self.value: str = value
        self.childs: list["Node"] = []

    def __repr__(self):
        s = f"Node({self.value})"
        for child in self.childs:
            s += f"\n\t-> Node({child.value})"
        return s


def parse(filename: str) -> list[str]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = fd.read().splitlines()

    # get all nodes
    nodes = dict()
    for line in lines:
        curr, _ = line.split(":")
        curr = curr.strip()
        if curr not in nodes:
            nodes[curr] = Node(curr)

    # add childs to all nodes
    for line in lines:
        curr, childs = line.split(":")
        curr = curr.strip()
        childs = childs.strip().split(' ')
        for child in childs:
            if child not in nodes.keys():
                nodes[child] = Node(child)
            nodes[curr].childs.append(nodes[child])

    return nodes


def solve_part1(root: Node) -> int:
    """Root is the 'you' node"""
    def f(node: Node):
        if node.value == "out":
            return 1
        elif not node:
            return 0
        res = 0
        for c in node.childs:
            res += f(c)
        return res
    x = f(root)
    return x

def solve_part2(root: Node) -> int:
    """Root is the 'svr' node"""
    @cache
    def f(node: Node, has_fft: bool, has_dac: bool) -> int:
        if node.value == "out" and has_fft and has_dac:
            return 1
        res = 0
        has_dac = has_dac or (node.value == "dac")
        has_fft = has_fft or (node.value == "fft")
        for c in node.childs:
            res += f(c, has_fft, has_dac)
        return res
    x = f(root, False, False)
    return x

if __name__ == "__main__":
    assert solve_part1(parse("example.txt")["you"]) == 5
    print(solve_part1(parse("input.txt")["you"]))
    assert solve_part2(parse("example2.txt")["svr"]) == 2
    print(solve_part2(parse("input.txt")["svr"]))
