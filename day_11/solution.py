from functools import cache


def blink(stone_vals: list[str]) -> list[str]:
    new_vals = []
    for val in stone_vals:
        if val == '0':
            new_vals.append('1')
        elif len(val) % 2 == 0:
            half = len(val) // 2
            fv = val[:half]
            sv = val[half:].lstrip('0')
            if not sv:
                sv = '0'
            new_vals.append(fv)
            new_vals.append(sv)
        else:
            new_vals.append(str(int(val) * 2024))
    return new_vals


@cache
def stones_num(val: str, blinks: int) -> int:
    if blinks == 0:
        return 1

    if val == '0':
        return stones_num('1', blinks - 1)
    if len(val) % 2 == 0:
        half = len(val) // 2
        fv = val[:half]
        sv = val[half:].lstrip('0')
        if not sv:
            sv = '0'
        return stones_num(fv, blinks - 1) + stones_num(sv, blinks - 1)
    return stones_num(str(int(val) * 2024), blinks - 1)


if __name__ == "__main__":
    path = "input.txt"

    with open(path, 'r') as f:
        data = f.read().strip()

    data = data.split()

    stone_vals = data[:]

    for i in range(25):
        stone_vals = blink(stone_vals)

    # Part 1
    print(len(stone_vals))

    stone_vals = data[:]

    total_stones = 0
    for v in stone_vals:
        total_stones += stones_num(v, 75)

    print(total_stones)
