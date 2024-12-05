from collections import defaultdict
from typing import Mapping, Collection


def read_and_parse(path: str) -> tuple[list[str], list[str]]:
    with open(path, 'r') as f:
        data = f.read()

    rules, updates = data.split('\n\n')

    rules = rules.split('\n')
    updates = updates.split('\n')

    return rules, updates


def is_correct(page_number_order: list[int], rules: Mapping[int, set]) -> bool:
    prev_occurrences = set()
    for pn in page_number_order:
        if rules[pn].intersection(prev_occurrences):
            return False
        prev_occurrences.add(pn)
    return True


def find_not_blocked(line: Collection[int], rules: Mapping[int, set]) -> int:
    line = set(line)

    for num in line:
        remaining = line - {num}
        # Is not 'blocked' by any other page
        if not rules[num].intersection(remaining):
            return num


def fix_line(line: list[int], rules: Mapping[int, set]):
    # We have to rearrange this, so there is no order right now
    line = set(line)

    # If an element is non blocked, it can be added at the end. We are going to find such elements one by one,
    # so this list will be reversed for now. We reverse it at the end in order to get correct page order.
    order_reversed = []
    remaining_elements = line
    while remaining_elements:
        not_blocked = find_not_blocked(remaining_elements, rules)
        remaining_elements = remaining_elements - {not_blocked}
        order_reversed.append(not_blocked)

    return order_reversed[::-1]


if __name__ == '__main__':
    path = 'input.txt'

    rules, updates = read_and_parse(path)

    if not updates[-1]:
        updates = updates[:-1]

    rules_dct = defaultdict(set)
    for rule in rules:
        pn, pn_prev = [int(i) for i in rule.split('|')]

        rules_dct[pn].add(pn_prev)

    updates = [[int(i) for i in update.split(',')] for update in updates]

    correct_middle_nums_sum = 0
    for line in updates:
        if is_correct(line, rules_dct):
            correct_middle_nums_sum += line[len(line) // 2]

    # Part 1
    print(correct_middle_nums_sum)

    corrected_middle_nums_sum = 0
    for line in updates:
        if not is_correct(line, rules_dct):
            corrected_line = fix_line(line, rules_dct)
            corrected_middle_nums_sum += corrected_line[len(corrected_line) // 2]

    # Part 2
    print(corrected_middle_nums_sum)
