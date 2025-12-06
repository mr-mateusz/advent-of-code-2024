def parse(schema: str) -> tuple[list, str]:
    schema = schema.strip().split('\n')

    if '#' in schema[0]:
        _type = 'l'
    else:
        _type = 'k'

    heights = [0 for _ in range(len(schema[0]))]
    for row in schema[1:-1]:
        for i, char in enumerate(row):
            if char == '#':
                heights[i] += 1
    return heights, _type


def fits(key: list, lock: list, max_height: int) -> bool:
    for k, l in zip(key, lock):
        if k + l > max_height:
            return False
    return True


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    keys_and_locks = data.split('\n\n')

    keys = []
    locks = []

    for schema in keys_and_locks:
        heights, _type = parse(schema)

        if _type == 'k':
            keys.append(heights)
        else:
            locks.append(heights)

    max_height = 5

    total = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock, max_height):
                total += 1

    # Part 1
    print(total)
