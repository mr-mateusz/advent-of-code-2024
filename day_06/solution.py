import time
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
    for _r in range(len(original_grid)):
        for _c in range(len(original_grid[0])):
            if grid[_r][_c] == '^':
                return Pos(_r, _c)
    return Pos(-1, -1)


def count_values(grid: list[list], value: Any) -> int:
    total = 0
    for r in range(len(original_grid)):
        for c in range(len(original_grid[0])):
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


def deepcopy(lst: list[list]) -> list[list]:
    return [line[:] for line in lst]


def simulate_movement(grid: list[list], start_pos: Pos) -> tuple[list[list], bool]:
    """Returned bool is an indication if guard is stuck in a loop."""
    grid = deepcopy(grid)

    pos = start_pos
    direction = Direction.N

    visited_positions = set()
    while pos.is_in(grid):
        visited_positions.add((pos, direction))
        grid[pos.r][pos.c] = 'X'
        pos, direction = move(grid, pos, direction)
        if (pos, direction) in visited_positions:
            # The guard is stuck in an infinite loop
            return grid, True

    return grid, False


def find_infinite_loops(original_grid: list[list], grid_with_movement: list[list], start_pos: Pos) -> int:
    grid_with_movement = deepcopy(grid_with_movement)

    # Starting position cannot be modified
    grid_with_movement[start_pos.r][start_pos.c] = '^'

    infinite_loops = 0
    for _r in range(len(original_grid)):
        for _c in range(len(original_grid[0])):
            # This field was visited by the guard in the original grid, so we can try to modify it
            if grid_with_movement[_r][_c] == 'X':
                original_grid_modified = deepcopy(original_grid)
                original_grid_modified[_r][_c] = '#'

                # Simulate the guard's movement
                _, is_stuck = simulate_movement(original_grid_modified, start_pos)
                if is_stuck:
                    infinite_loops += 1

    return infinite_loops


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = [l.strip() for l in f.readlines()]

    original_grid = [list(l) for l in data]

    start = find_start(original_grid)

    grid_with_movement, _ = simulate_movement(original_grid, start)

    total = count_values(grid_with_movement, 'X')

    # Part 1
    print(total)

    st = time.perf_counter()

    infinite_loops = find_infinite_loops(original_grid, grid_with_movement, start)

    print(f'Time: {time.perf_counter() - st}')

    # part 2
    print(infinite_loops)
