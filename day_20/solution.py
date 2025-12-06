from __future__ import annotations

from collections import Counter, deque
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


def shortest_path(start_pos: Pos, end_pos: Pos, grid_size: tuple[int, int],
                  byte_positions: Collection[Pos]) -> int | None:
    nodes_to_check = deque()
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


if __name__ == "__main__":
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [l.strip() for l in f]

    grid_size = (len(data), len(data[0]))
    start_pos = None
    end_pos = None
    taken_positions = []

    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == 'S':
                start_pos = Pos(r, c)
            if data[r][c] == 'E':
                end_pos = Pos(r, c)
            if data[r][c] == '#':
                taken_positions.append(Pos(r, c))

    print(start_pos, end_pos)

    taken_positions = set(taken_positions)

    original_shortest_path_len = shortest_path(start_pos, end_pos, grid_size, taken_positions)

    modified_shortest_paths_len = []
    for i, p in enumerate(taken_positions):
        print(f'{i + 1}/{len(taken_positions)}')

        if not ((p + (0, 1) not in taken_positions and p + (0, -1) not in taken_positions) or
                (p + (1, 0) not in taken_positions and p + (-1, 0) not in taken_positions)):
            continue

        _taken_positions = taken_positions - set([p])

        modified_shortest_paths_len.append(shortest_path(start_pos, end_pos, grid_size, _taken_positions))

    cnt = Counter(original_shortest_path_len - l for l in modified_shortest_paths_len if l < original_shortest_path_len)

    total = 0
    for k, v in cnt.items():
        if k >= 100:
            total += v

    # Part 1
    print(total)

    # print(cnt)
