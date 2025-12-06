from __future__ import annotations

import time
from collections import Counter, deque
from functools import cache
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


@cache
def shortest_path(start_pos: Pos, end_pos: Pos, grid_size: tuple[int, int],
                  byte_positions: frozenset[Pos], max_check: int | None = None) -> int | None:
    nodes_to_check = deque()
    nodes_to_check.append((start_pos, 0))

    already_visited = set()
    while nodes_to_check:
        node, current_dist = nodes_to_check.popleft()
        if node in already_visited:
            continue

        if max_check is not None and current_dist > max_check:
            return None

        already_visited.add(node)

        if node == end_pos:
            return current_dist

        for neighbour in get_reachable_neighbours(node, grid_size, byte_positions):
            if neighbour not in already_visited:
                nodes_to_check.append((neighbour, current_dist + 1))
    return None


def get_all_jumps(pos: Pos, max_jump: int) -> list[(Pos, int)]:
    jumps = []
    for current_jump in range(1, max_jump + 1):
        for dim1 in range(current_jump + 1):
            dim2 = current_jump - dim1
            jumps.extend([
                (pos + (dim1, dim2), current_jump),
                (pos + (dim1, -dim2), current_jump),
                (pos + (-dim1, dim2), current_jump),
                (pos + (-dim1, -dim2), current_jump)
            ])
    return list(set(jumps))


def isin(pos: Pos, grid_size: tuple[int, int]) -> bool:
    return 0 <= pos.r < grid_size[0] and 0 <= pos.c < grid_size[1]


def possible_jumps(pos: Pos, max_jump: int, grid_size: tuple[int, int], byte_positions: Collection[Pos]) \
        -> list[tuple[Pos, int]]:
    if max_jump < 1:
        return []

    all_jumps = get_all_jumps(pos, max_jump)

    all_jumps = [j for j in all_jumps if isin(j[0], grid_size)]
    all_jumps = [j for j in all_jumps if j[0] not in byte_positions]

    return all_jumps


def get_all_path_distances_with_cheat(start_pos: Pos, end_pos: Pos, grid_size: tuple[int, int],
                                      byte_positions: frozenset[Pos], cheat_max_jump: int,
                                      max_dist_check: int):
    nodes_to_check = deque()
    nodes_to_check.append((start_pos, 0))

    already_visited = set()
    all_distances = []
    while nodes_to_check:
        node, current_dist = nodes_to_check.popleft()
        if node in already_visited:
            continue

        already_visited.add(node)

        for cheat_end_pos, cheat_dist in possible_jumps(node, cheat_max_jump, grid_size, byte_positions):
            if current_dist + cheat_dist > max_dist_check:
                continue

            shortest_path_from_cheat_end = shortest_path(cheat_end_pos, end_pos, grid_size, byte_positions, None)

            if shortest_path_from_cheat_end + current_dist + cheat_dist <= max_dist_check:
                all_distances.append(current_dist + cheat_dist + shortest_path_from_cheat_end)

        if current_dist == max_dist_check:
            break

        for neighbour in get_reachable_neighbours(node, grid_size, byte_positions):
            if neighbour not in already_visited:
                nodes_to_check.append((neighbour, current_dist + 1))

    return all_distances


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

    taken_positions = frozenset(taken_positions)

    original_shortest_path_len = shortest_path(start_pos, end_pos, grid_size, taken_positions)

    max_cheat_len = 20
    min_picoseconds_gain = 100

    st = time.perf_counter()
    all_distances = get_all_path_distances_with_cheat(start_pos, end_pos, grid_size,
                                                      taken_positions, max_cheat_len, original_shortest_path_len)

    print('time:', time.perf_counter() - st)

    picoseconds_gain = [original_shortest_path_len - d for d in all_distances if
                        original_shortest_path_len - d >= min_picoseconds_gain]

    cnt = Counter(picoseconds_gain)

    tmp = [(k, v) for k, v in cnt.items() if k >= 1]

    tmp = list(sorted(tmp, key=lambda x: x[0]))

    total = 0
    for k, v in tmp:
        total += v
        # print(v, 'cheats ', k, 'picoseconds')
    print('total', total)
