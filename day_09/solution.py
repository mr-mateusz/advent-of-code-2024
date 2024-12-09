def expand(disk_dense: str, first_block_data: bool = True) -> list[int]:
    is_data_block = first_block_data

    disk_expanded = []
    _id = 0
    for block_len in disk_dense:
        block_len = int(block_len)

        if is_data_block:
            disk_expanded.extend([_id] * block_len)
            _id += 1
        else:
            disk_expanded.extend([-1] * block_len)
        is_data_block = not is_data_block

    return disk_expanded


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
        if value == -1:
            return res
        res += index * value
    return res


if __name__ == '__main__':
    path = "input.txt"

    with open(path, 'r') as f:
        data = f.read().strip()

    disk_expanded = expand(data, True)
    disk_compacted = compact(disk_expanded)

    # Part 1
    print(checksum(disk_compacted))
