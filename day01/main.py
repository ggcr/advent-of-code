import os


def parse(filename: str) -> list[str]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        return fd.readlines()


def solve_part1(instructions: list[str]) -> int:
    res = 0
    dial = 50
    for instruction in instructions:
        direction, ticks = instruction[0], int(instruction[1:])

        if direction == "L":
            dial = (dial - ticks) % 100
        elif direction == "R":
            dial = (dial + ticks) % 100
        else:
            raise ValueError(f"Bad direction: '{direction}'")

        if dial == 0:
            res += 1

    return res

def solve_part2(instructions: list[str]) -> int:
    res = 0
    dial = 50
    for instruction in instructions:
        direction, ticks = instruction[0], int(instruction[1:])
        d = -1 if direction == "L" else 1
        for _ in range(ticks):
            dial = (dial + d) % 100
            if dial == 0:
                res+=1
    return res

if __name__ == "__main__":
    assert solve_part1(parse("example.txt")) == 3
    print(solve_part1(parse("input.txt")))
    assert solve_part2(parse("example.txt")) == 6
    print(solve_part2(parse("input2.txt")))

