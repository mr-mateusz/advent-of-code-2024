from enum import Enum
from typing import Any, NamedTuple


class Pos(NamedTuple):
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c + other.c)

    def is_in(self, grid: list[list]) -> bool:
        max_r = len(grid)
        max_c = len(grid[0])

        return 0 <= self.r < max_r and 0 <= self.c < max_c


class Direction(Enum):
    N = Pos(-1, 0)
    E = Pos(0, 1)
    S = Pos(1, 0)
    W = Pos(0, -1)

    def rotate(self):
        members = list(Direction)
        return members[(members.index(self) + 1) % len(members)]


def find_start(grid: list[list]) -> Pos:
    for _r in range(len(data)):
        for _c in range(len(data[0])):
            if grid[_r][_c] == '^':
                return Pos(_r, _c)
    return Pos(-1, -1)


def count_values(grid: list[list], value: Any) -> int:
    total = 0
    for r in range(len(data)):
        for c in range(len(data[0])):
            if grid[r][c] == value:
                total += 1
    return total


def move(grid: list[list], pos: Pos, direction: Direction) -> tuple[Pos, Direction]:
    next_move = pos + direction.value
    try:
        while grid[next_move.r][next_move.c] == '#':
            direction = direction.rotate()
            next_move = pos + direction.value
    except IndexError:
        pass
    return next_move, direction


def simulate_movement(grid: list[list], start_pos: Pos) -> list[list]:
    grid = [line[:] for line in grid]

    pos = start_pos
    direction = Direction.N

    while pos.is_in(grid):
        grid[pos.r][pos.c] = 'X'
        pos, direction = move(grid, pos, direction)

    return grid


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = [l.strip() for l in f.readlines()]

    data = [list(l) for l in data]

    start = find_start(data)

    grid_with_movement = simulate_movement(data, start)

    total = count_values(grid_with_movement, 'X')

    # Part 1
    print(total)
