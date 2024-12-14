from collections import Counter
from math import prod
from typing import Sequence


def parse_line(line: str) -> tuple[tuple, tuple]:
    p, v = line.split()
    p1, p2 = [int(value) for value in p.strip('p').strip('=').split(',')]
    v1, v2 = [int(value) for value in v.strip('v').strip('=').split(',')]
    return (p2, p1), (v2, v1)


def move(pos: tuple, vel: tuple, grid_shape: tuple) -> tuple:
    p0 = pos[0] + vel[0]
    p1 = pos[1] + vel[1]

    while p0 < 0:
        p0 += grid_shape[0]
    while p1 < 0:
        p1 += grid_shape[1]
    while p0 >= grid_shape[0]:
        p0 -= grid_shape[0]
    while p1 >= grid_shape[1]:
        p1 -= grid_shape[1]

    return p0, p1


def simulate(positions: Sequence[tuple], velocities: Sequence[tuple], grid_shape: tuple, n: int) -> list[tuple]:
    for i in range(n):
        positions = [move(pos, vel, grid_shape) for pos, vel in zip(positions, velocities)]
    return positions


def calculate_sf(positions: Sequence[tuple], grid_shape: tuple) -> int:
    qdrants_cnt = {}

    for p0, p1 in positions:
        if p0 == grid_shape[0] // 2:
            continue
        elif 0 <= p0 < grid_shape[0] // 2:
            q0 = 0
        else:
            q0 = 1

        if p1 == grid_shape[1] // 2:
            continue
        elif 0 <= p1 < grid_shape[1] // 2:
            q1 = 0
        else:
            q1 = 1

        try:
            qdrants_cnt[(q0, q1)] += 1
        except KeyError:
            qdrants_cnt[(q0, q1)] = 1

    return prod(qdrants_cnt.values())


def print_grid(positions: Sequence[tuple], shape: tuple) -> None:
    counter = Counter(positions)

    grid = [[0 for _ in range(shape[1])] for _ in range(shape[0])]

    for k, v in counter.items():
        grid[k[0]][k[1]] = v

    for line in grid:
        print(line)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        lines = [l.strip() for l in f]

    grid_shape = (103, 101)

    lines_parsed = [parse_line(l) for l in lines]

    positions, velocities = list(zip(*lines_parsed))

    n = 100

    pos_100 = simulate(positions, velocities, grid_shape, n)

    safety_factor = calculate_sf(pos_100, grid_shape)

    # Part 1
    print(safety_factor)
