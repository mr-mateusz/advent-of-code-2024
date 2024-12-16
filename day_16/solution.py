from __future__ import annotations

from enum import Enum
from itertools import count
from queue import PriorityQueue
from typing import NamedTuple


class Pos(NamedTuple):
    r: int
    c: int

    def __add__(self, other):
        return Pos(self.r + other.r, self.c + other.c)


class GraphPosition(NamedTuple):
    pos: Pos
    direction: Direction

    def turn_right(self) -> GraphPosition:
        return GraphPosition(self.pos, self.direction.turn_right())

    def turn_left(self) -> GraphPosition:
        return GraphPosition(self.pos, self.direction.turn_left())

    def move_forward(self) -> GraphPosition:
        return GraphPosition(self.pos + self.direction.value, self.direction)


class Direction(Enum):
    N = Pos(-1, 0)
    E = Pos(0, 1)
    S = Pos(1, 0)
    W = Pos(0, -1)

    def turn_right(self) -> Direction:
        members = list(Direction)
        return members[(members.index(self) + 1) % len(members)]

    def turn_left(self) -> Direction:
        members = list(Direction)
        return members[(members.index(self) - 1) % len(members)]


def find_one(data: list[str], value: str) -> Pos | None:
    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == value:
                return Pos(r, c)
    return None


def get_neighbours(data: list[str], graph_pos: GraphPosition) -> list[tuple[GraphPosition, int]]:
    MOVE_COST = 1
    TURN_COST = 1000

    forward_pos = graph_pos.move_forward()

    neighbours = []
    if data[forward_pos.pos.r][forward_pos.pos.c] != '#':
        neighbours.append((forward_pos, MOVE_COST))

    neighbours.append((graph_pos.turn_left(), TURN_COST))
    neighbours.append((graph_pos.turn_right(), TURN_COST))

    return neighbours


def shortest_path_len(data: list[str]) -> int:
    start_pos = find_one(data, 'S')
    start_pos = GraphPosition(start_pos, Direction.E)

    end_pos = find_one(data, 'E')

    print(start_pos, end_pos)

    tiebreaker = count()

    distances = {
        start_pos: 0
    }
    visited = set()

    to_visit = PriorityQueue()
    to_visit.put((0, next(tiebreaker), start_pos))

    while to_visit:
        current_dist, _, current_pos = to_visit.get()

        # We add the multiple times instead of updating distances (priorities) in the priority queue
        if current_pos in visited:
            continue

        if current_pos.pos == end_pos:
            return current_dist

        for neighbour_pos, dist in get_neighbours(data, current_pos):
            dist_via_current = current_dist + dist

            if neighbour_pos in distances:
                if distances[neighbour_pos] > dist_via_current:
                    distances[neighbour_pos] = dist_via_current
                    to_visit.put((dist_via_current, next(tiebreaker), neighbour_pos))
            else:
                distances[neighbour_pos] = dist_via_current
                to_visit.put((dist_via_current, next(tiebreaker), neighbour_pos))

        visited.add(current_pos)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [l.strip() for l in f]

    # Part 1
    print(shortest_path_len(data))
