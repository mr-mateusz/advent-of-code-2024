def is_safe(row: list[int], min_dif: int, max_dif: int) -> bool:
    if not row:
        return True

    _prev = row[0]
    for _next in row[1:]:
        _diff = _prev - _next
        if not min_dif <= _diff <= max_dif:
            return False
        _prev = _next
    return True


def is_row_safe(row: list[int]) -> bool:
    return is_safe(row, -3, -1) or is_safe(row, 1, 3)


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = [l.strip() for l in f.readlines()]

    data = [[int(n) for n in row.split()] for row in data]

    # Part 1
    print(sum([is_row_safe(row) for row in data]))
