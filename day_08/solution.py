from __future__ import annotations

from typing import NamedTuple


class Pos(NamedTuple):
    r: int
    c: int

    def __add__(self, other) -> Pos:
        return Pos(self.r + other.r, self.c + other.c)

    def __sub__(self, other) -> Pos:
        return Pos(self.r - other.r, self.c - other.c)

    def is_in(self, data: list[str]) -> bool:
        return 0 <= self.r < len(data) and 0 <= self.c < len(data[0])


def count_antinodes(data: list[str]) -> int:
    # Get antennas positions
    antennas_positions = {}
    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] != '.':
                try:
                    antennas_positions[data[r][c]].append(Pos(r, c))
                except KeyError:
                    antennas_positions[data[r][c]] = [Pos(r, c)]

    antinode_positions = set()
    for antenna_type, positions in antennas_positions.items():
        for pos in positions:
            for other_pos in positions:
                if pos == other_pos:
                    continue
                dist = other_pos - pos
                antinode_pos = other_pos + dist
                if antinode_pos.is_in(data):
                    antinode_positions.add(antinode_pos)
    return len(antinode_positions)


if __name__ == "__main__":
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [l.strip() for l in f.readlines()]

    res = count_antinodes(data)

    # Part 1
    print(res)
