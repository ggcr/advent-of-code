import os
import numpy as np


def parse(filename: str) -> dict:
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), filename), "r+"
    ) as fd:
        lines = fd.read().splitlines()

    regions = list() # "4x4": [shape1, shape2]

    shapes = []
    b = False
    shape = []

    for l in lines:
        # shape
        if ':' in l and l.split(':')[-1].strip() == '':
            b = not b
            continue
        elif l.strip() == '':
            shapes.append(shape)
            shape = []
            b = not b
            continue
        if 'x' not in l:
            lx = l.replace(".", "0").replace("#", "1")
            shape.append(list(map(int, list(lx))))

        # regions
        if 'x' in l:
            shape_i = 0
            regions.append([l.split(':')[0]])
            for i in l.split(':')[-1].strip().split(' '):
                if i == 0 :
                    continue
                for j in range(int(i)):
                    regions[-1].append(np.array(shapes[shape_i]))
                shape_i += 1

    return regions

def solve_part1(regions: list) -> int:
    res = 0
    for region in regions:
        dims, shapes = region[0], region[1:]
        area_grid = int(dims.split('x')[0]) * int(dims.split('x')[1])
        area_shapes = sum(s.shape[0]*s.shape[1] for s in shapes)
        print(area_grid, area_shapes)
        if area_grid >= area_shapes:
            res += 1
    return res


if __name__ == "__main__":
    print(solve_part1(parse("input.txt")))
