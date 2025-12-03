import os
from functools import lru_cache


def parse(filename: str) -> list[str]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        data = fd.readlines()
        return [d.strip() for d in data]


def solve_part1(batteries: list[str]) -> int:
    res = 0
    for bank in batteries:
        maxBank = 0
        for i in range(len(bank) - 1):
            for j in range(i + 1, len(bank)):
                num = int(bank[i] + bank[j])
                maxBank = max(maxBank, num)
        res += maxBank
    return res


def solve_part2(batteries: list[str]) -> int:
    res = 0
    for bank in batteries:
        # rephrasing this as:
        # "get all possible substrings of length K"
        @lru_cache(maxsize=None)
        def f(i: int, length: int):
            if length == 12:
                return ""
            needed = 12 - length
            left = len(bank) - i
            if i == len(bank) or (left < needed):
                return "-1"
            skip = f(i + 1, length)
            take = bank[i] + f(i + 1, length + 1)
            return max(take, skip)

        x = f(0, 0)
        print(x)
        res += int(x)
    return res



if __name__ == "__main__":
    assert solve_part1(parse("example.txt")) == 357
    print(solve_part1(parse("input.txt")))
    assert solve_part2(parse("example.txt")) == 3121910778619
    print(solve_part2(parse("input.txt")))
