from __future__ import annotations

import collections
from typing import NamedTuple, Collection


class Pos(NamedTuple):
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other[0], self.c + other[1])

    @classmethod
    def from_xy_str(cls, pos: str) -> Pos:
        pos = [int(val) for val in pos.split(',')]
        return Pos(pos[1], pos[0])


def get_neighbours(node: Pos) -> list[Pos]:
    neighbours = []
    for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbours.append(node + direction)
    return neighbours


def get_reachable_neighbours(node: Pos, grid_size: tuple[int, int], byte_positions: Collection[Pos]) -> list[Pos]:
    neighbours = []
    for n in get_neighbours(node):
        if 0 <= n.r < grid_size[0] and 0 <= n.c < grid_size[1] and n not in byte_positions:
            neighbours.append(n)
    return neighbours


def shortest_path(start_pos: Pos, end_pos: Pos, grid_size: tuple[int, int], byte_positions: list[Pos]) -> int | None:
    nodes_to_check = collections.deque()
    nodes_to_check.append((start_pos, 0))

    byte_positions = set(byte_positions)

    already_visited = set()
    while nodes_to_check:
        node, current_dist = nodes_to_check.popleft()
        if node in already_visited:
            continue

        already_visited.add(node)

        if node == end_pos:
            return current_dist

        for neighbour in get_reachable_neighbours(node, grid_size, byte_positions):
            if neighbour not in already_visited:
                nodes_to_check.append((neighbour, current_dist + 1))
    return None


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [l.strip() for l in f.readlines()]

    # grid_size = (7, 7)
    grid_size = (71, 71)

    n_bytes_fallen = 1024

    start_pos = Pos(0, 0)
    end_pos = Pos(grid_size[0] - 1, grid_size[1] - 1)

    byte_positions = [Pos.from_xy_str(pos) for pos in data]

    # Part 1
    print(shortest_path(start_pos, end_pos, grid_size, byte_positions[:n_bytes_fallen]))

    # Part 2
    while True:
        shortest_path_len = shortest_path(start_pos, end_pos, grid_size, byte_positions[:n_bytes_fallen])

        if shortest_path_len is None:
            blocking_byte_pos = byte_positions[n_bytes_fallen - 1]
            print(n_bytes_fallen - 1)
            print(f'{blocking_byte_pos.c},{blocking_byte_pos.r}')
            break

        n_bytes_fallen += 1
