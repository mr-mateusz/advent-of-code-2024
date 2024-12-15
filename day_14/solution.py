from math import prod
from typing import Sequence

import matplotlib.pyplot as plt


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


def simulate(positions: Sequence[tuple], velocities: Sequence[tuple], grid_shape: tuple, n: int) -> list[list[tuple]]:
    history = [positions]

    for i in range(n):
        print(i)
        positions = [move(pos, vel, grid_shape) for pos, vel in zip(positions, velocities)]
        history.append(positions)
    return history


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
    grid = [['.' for _ in range(shape[1])] for _ in range(shape[0])]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in set(positions):
                grid[i][j] = '#'

    grid = [''.join(line) for line in grid]

    for line in grid:
        print(line)


def find_longest_line(vals: list[int]) -> int:
    if not vals:
        return 0
    last_val = vals[0]
    longest_line = 0
    current_line = 1
    for val in vals[1:]:
        if val == last_val + 1:
            current_line += 1
        else:
            if current_line > longest_line:
                longest_line = current_line
            current_line = 1
        last_val = val
    if current_line > longest_line:
        longest_line = current_line
    return longest_line


def find_longest_robot_vertical_line(positions: list[tuple], shape: tuple) -> int:
    n_cols = shape[1]
    longest_line = 0
    for i in range(n_cols):
        vals_in_col = [p[0] for p in positions if p[1] == i]
        vals_in_col = sorted(vals_in_col)
        longest_col_line = find_longest_line(vals_in_col)
        if longest_col_line > longest_line:
            longest_line = longest_col_line
    return longest_line


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        lines = [l.strip() for l in f]

    grid_shape = (103, 101)
    part_1_n = 100
    sumulation_steps = 10_000

    lines_parsed = [parse_line(l) for l in lines]
    positions, velocities = list(zip(*lines_parsed))

    # initial state is included in the history
    positions_history = simulate(positions, velocities, grid_shape, sumulation_steps)

    safety_factor = calculate_sf(positions_history[part_1_n], grid_shape)

    # Part 1
    print(safety_factor)

    # Let's analyze the history somehow and look for a pattern
    longest_robot_vertical_line = []
    for positions_step in positions_history:
        longest_robot_vertical_line.append(find_longest_robot_vertical_line(positions_step, grid_shape))

    longest_lines = sorted(enumerate(longest_robot_vertical_line), key=lambda x: x[1], reverse=True)[:10]

    print(longest_lines)

    plt.plot(longest_robot_vertical_line)

    plt.savefig("plot.png")
    print("Plot saved as plot.png")

    print_grid(positions_history[longest_lines[0][0]], grid_shape)

    # Part 2
    print(longest_lines[0][0])
