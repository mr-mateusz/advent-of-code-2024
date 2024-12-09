from __future__ import annotations

from typing import NamedTuple


class Block(NamedTuple):
    value: int
    start_idx: int
    size: int


def expand(disk_dense: str, first_block_data: bool = True) -> list[int]:
    is_data_block = first_block_data

    disk_expanded = []
    _id = 0
    block_ids_and_positions = []
    start_idx = 0
    for block_len in disk_dense:
        block_len = int(block_len)

        if is_data_block:
            disk_expanded.extend([_id] * block_len)
            block_ids_and_positions.append(Block(_id, start_idx, block_len))
            _id += 1
        else:
            disk_expanded.extend([-1] * block_len)
        is_data_block = not is_data_block
        start_idx += block_len

    return disk_expanded, block_ids_and_positions


def compact(disk_expanded: list[int]) -> list[int]:
    disk = disk_expanded[:]
    p1 = 0
    p2 = len(disk) - 1

    while p1 < p2:
        try:
            while disk[p1] != -1:
                p1 += 1
            while disk[p2] == -1:
                p2 -= 1
        except IndexError:
            break
        if p1 < p2:
            disk[p1], disk[p2] = disk[p2], disk[p1]
    return disk


def checksum(disk_expanded: list[int]) -> int:
    res = 0
    for index, value in enumerate(disk_expanded):
        if value != -1:
            res += index * value
    return res


def find_first_gap(disk_expanded: list[int], size: int, stop_at: int) -> int | None:
    counter = 0
    start = -1
    for index, val in enumerate(disk_expanded):
        if index >= stop_at:
            return None
        if val == -1:
            if start == -1:
                start = index
            counter += 1
            if counter == size:
                return start
        else:
            start = -1
            counter = 0
    return None


def put(disk_expanded: list[int], start_pos: int, size: int, value: int) -> None:
    for index in range(start_pos, start_pos + size):
        disk_expanded[index] = value


def compact_blocks(disk_expanded: list[int], blocks: list[Block]) -> list[int]:
    disk_expanded = disk_expanded[:]
    while blocks:
        # Start from the end
        block = blocks.pop()

        gap_start_idx = find_first_gap(disk_expanded, block.size, block.start_idx)

        if gap_start_idx:
            put(disk_expanded, block.start_idx, block.size, -1)
            put(disk_expanded, gap_start_idx, block.size, block.value)
    return disk_expanded


if __name__ == '__main__':
    path = "input.txt"

    with open(path, 'r') as f:
        data = f.read().strip()

    # blocks are for part 2
    disk_expanded, blocks = expand(data, True)
    disk_compacted = compact(disk_expanded)

    # Part 1
    print(checksum(disk_compacted))

    # print(disk_expanded)

    # print(blocks)

    disk_compacted = compact_blocks(disk_expanded, blocks)

    # print(disk_compacted)

    # Part 2
    print(checksum(disk_compacted))
