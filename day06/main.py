import os
from functools import reduce


def parse(filename: str) -> tuple[list[int], list[str]]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = fd.read().splitlines()
        nums, operators = lines[:-1], lines[-1]
        for i in range(len(nums)):
            nums[i] = list(map(int, nums[i].split()))
        return nums, operators.split()


def crop_positions(operators: str) -> list[int]:
    """A dummy bad helper to know the positions of
    operators so we know where we need to crop each row of numbers"""
    return [i for i, ch in enumerate(operators) if ch != " "] + [len(operators) + 1]


def parse_part2(filename: str) -> tuple[list[list[str]], list[str]]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = fd.read().splitlines()
        nums, operators = lines[:-1], lines[-1]
        op_pos = crop_positions(operators)
        for k in range(len(nums)):
            vals: list[str] = []
            for i in range(len(op_pos) - 1):
                op1, op2 = op_pos[i], op_pos[i + 1]
                vals.append(nums[k][op1 : op2 - 1])
            nums[k] = vals
        return nums, operators.split()


def solve_part1(nums: list[int], operators: list[str]) -> int:
    res = 0
    t_nums = list(map(list, zip(*nums)))
    for i, op in enumerate(operators):
        if op == "+":
            res += sum(t_nums[i])
        elif op == "-":
            res += sum(map(lambda x: x * -1, t_nums[i]))
        elif op == "*":
            res += reduce(lambda x, y: x * y, t_nums[i], 1)
        else:
            raise ValueError(f"Op not recognized: {op}")
    return res


def solve_part2(nums: list[list[str]], operators: list[str]) -> int:
    # transpose
    t_nums = list(map(list, zip(*nums)))

    # the important bit here is the `expr` lambda
    # where we get the -N position of all the numbers
    for idx in range(len(t_nums)):
        N = list(map(str, t_nums[idx]))
        m = max(map(len, N))
        values: list[int] = []
        for i in range(1, m + 1):
            expr = map(lambda n: n[-i] if len(n) >= i else "", N)
            val = int(str("".join(expr)))
            values.append(val)
        t_nums[idx] = values

    res = 0
    for i, op in enumerate(operators):
        if op == "+":
            res += sum(t_nums[i])
        elif op == "-":
            res += sum(map(lambda x: x * -1, t_nums[i]))
        elif op == "*":
            res += reduce(lambda x, y: x * y, t_nums[i], 1)
        else:
            raise ValueError(f"Op not recognized: {op}")

    return res


if __name__ == "__main__":
    assert solve_part1(*parse("example.txt")) == 4277556
    print(solve_part1(*parse("input.txt")))
    assert solve_part2(*parse_part2("example.txt")) == 3263827
    print(solve_part2(*parse_part2("input.txt")))
