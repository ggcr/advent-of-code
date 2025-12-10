import copy
import os
from tqdm import tqdm
from functools import cache


def parse(filename: str) -> tuple[list[list[set]], list[set], list[list]]:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        buttons: list[list[set]] = []
        targets: list[set] = []
        voltages: list[list[int]] = []

        for line in fd.read().splitlines():
            goal = set()
            voltage = list()
            row_buttons = []

            for element in line.split(" "):
                # indicator lights
                if element.startswith("["):
                    for i, ch in enumerate(element[1:-1]):
                        if ch == "#":
                            goal.add(i)
                # list of available buttons
                if element.startswith("("):
                    button_press = set()
                    for num in element[1:-1].split(","):
                        button_press.add(int(num))
                    row_buttons.append(button_press)
                # voltage requirements
                if element.startswith("{"):
                    for num in element[1:-1].split(","):
                        voltage.append(int(num))

            targets.append(goal)
            buttons.append(row_buttons)
            voltages.append(voltage)

        return buttons, targets, voltages

def solve_part1(
    all_buttons: list[list[set]], targets: list[set], voltages: list[list[int]]
) -> int:
    total = 0

    for k in range(len(targets)):
        buttons = all_buttons[k]
        goal = targets[k]

        def f(s: set[int], i: int, pressed: int):
            # Base case: early return
            if s == goal and pressed > 0:
                return pressed

            # Base case: exhausted all options
            if i >= len(buttons):
                return None

            best = float("inf")

            # Complex case 1: we do not press this button
            res = f(s, i + 1, pressed)
            if res is not None:
                best = min(best, res)

            # Complex case 2: we press this button
            res = f(s ^ buttons[i], i + 1, pressed + 1)
            if res is not None:
                best = min(best, res)

            return best

        best = float("inf")
        for _ in range(len(buttons)):
            got = f(set([]), 0, 0)
            buttons = buttons[1:] + [buttons[0]]
            if got is not None:
                best = min(best, got)

        total += best

    if total == float("inf"):
        raise ValueError("not a valid solution found")

    return int(total)

def solve_part2(
    all_buttons: list[list[set]], targets: list[set], voltages: list[list[int]]
) -> int:
    total = 0

    for k in tqdm(range(len(targets))):
        buttons = all_buttons[k]
        voltage = tuple(voltages[k])

        @cache
        def f(i: int, v: tuple[int, ...]):
            # Base case: early return
            if v == voltage:
                return 0

            # Base case: exhausted all options
            if i >= len(buttons):
                return None

            # Base case: voltage requirement exceeded
            for iv in range(len(v)):
                if v[iv] > voltage[iv]:
                    return None

            best = float("inf")

            # Complex case 1: we do not press this button
            res = f(i + 1, v)
            if res is not None:
                best = min(best, res)

            # Complex case 2: we press this button and go to the next
            v2 = list(v)
            for ix in buttons[i]:
                v2[ix] += 1
            res = f(i + 1, tuple(v2))
            if res is not None:
                best = min(best, res + 1)

            # Complex case 3: we press this button and remain on the current
            v3 = list(v)
            for ix in buttons[i]:
                v3[ix] += 1
            res = f(i, tuple(v3))
            if res is not None:
                best = min(best, res + 1)

            return best

        total += f(0, tuple([0]*len(voltage)))

    if total == float("inf"):
        raise ValueError("not a valid solution found")

    return int(total)




if __name__ == "__main__":
    assert solve_part1(*parse("example.txt")) == 7
    print(solve_part1(*parse("input.txt")))
    assert solve_part2(*parse("example.txt")) == 33
    print(solve_part2(*parse("input.txt")))
