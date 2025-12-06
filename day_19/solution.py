from functools import cache
from typing import Collection


@cache
def is_pattern_possible(pattern: str, towels: Collection[str]) -> bool:
    if pattern in towels:
        return True

    if len(pattern) == 1:
        return False

    for i in range(1, len(pattern)):
        if is_pattern_possible(pattern[:i], towels) and is_pattern_possible(pattern[i:], towels):
            return True

    return False


@cache
def possible_arrangements_num(pattern: str, towels: Collection[str]) -> int:
    if pattern in towels:
        # Check if towel pattern can be made of other towels.
        # {'br', 'b', 'b'} -> 'br' can be made from 'br' but also 'b' and 'r'
        if len(pattern) > 1:
            towels_without_pattern = frozenset(set(towels) - {pattern})
            return 1 + possible_arrangements_num(pattern, towels_without_pattern)
        return 1

    if len(pattern) == 1:
        return 0

    total_arrangements = 0
    for i in range(1, len(pattern)):
        pattern_left = pattern[:i]

        if pattern_left in towels:
            total_arrangements += possible_arrangements_num(pattern[i:], towels)

    return total_arrangements


if __name__ == "__main__":
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    towels, patterns_to_display = data.split('\n\n')

    towels = frozenset(towels.strip().split(', '))
    patterns_to_display = patterns_to_display.strip().split('\n')

    # Part 1
    print(sum(is_pattern_possible(p, towels) for p in patterns_to_display))

    # Part 1 using part 2 code
    print(sum(possible_arrangements_num(p, towels) > 0 for p in patterns_to_display))

    # Part 2
    print(sum(possible_arrangements_num(p, towels) for p in patterns_to_display))
