from typing import Sequence


def get_neighbours(pos) -> list[tuple]:
    r, c = pos
    return [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1)
    ]


class Region:
    def __init__(self, garden_plots: set[tuple]):
        self.garden_plots = garden_plots

    def area(self) -> int:
        return len(self.garden_plots)

    def perimeter(self) -> int:
        total_perimeter = 0
        for plot in self.garden_plots:
            total_perimeter += len(set(get_neighbours(plot)).difference(self.garden_plots))
        return total_perimeter


def is_in(pos: Sequence[int], data: list[str]) -> bool:
    return 0 <= pos[0] < len(data) and 0 <= pos[1] < len(data[0])


def process_new_region(data: list[str], initial_pos: tuple[int, int]) -> Region:
    to_check = [initial_pos]
    already_checked = set()

    region_type = data[initial_pos[0]][initial_pos[1]]
    region_tiles = set()
    while to_check:
        current = to_check.pop()
        already_checked.add(current)
        if data[current[0]][current[1]] == region_type:
            region_tiles.add(current)
        else:
            continue
        for n in get_neighbours(current):
            if is_in(n, data) and n not in already_checked:
                to_check.append(n)
    return Region(region_tiles)


def find_regions(data: list[str]) -> list[Region]:
    already_assigned = set()
    regions = []
    for r in range(len(data)):
        for c in range(len(data[0])):
            if (r, c) not in already_assigned:
                new_region = process_new_region(data, (r, c))
                regions.append(new_region)
                already_assigned.update(new_region.garden_plots)
            else:
                already_assigned.add((r, c))
    return regions


if __name__ == '__main__':
    path = "input.txt"

    with open(path, 'r') as f:
        data = [l.strip() for l in f.readlines()]

    regions = find_regions(data)

    total_price = 0
    for r in regions:
        total_price += r.area() * r.perimeter()

    # Part 1
    print(total_price)
