from typing import Mapping


def read_and_parse(path: str) -> tuple[list[str], list[str]]:
    with open(path, 'r') as f:
        data = f.read()

    rules, updates = data.split('\n\n')

    rules = rules.split('\n')
    updates = updates.split('\n')

    return rules, updates


def is_correct(page_number_order: list[int], rules: Mapping[int, set]):
    prev_occurrences = set()
    for pn in page_number_order:
        if rules.setdefault(pn, set()).intersection(prev_occurrences):
            return False
        prev_occurrences.add(pn)
    return True


if __name__ == '__main__':
    path = 'input.txt'

    rules, updates = read_and_parse(path)

    if not updates[-1]:
        updates = updates[:-1]

    rules_dct = {}
    for rule in rules:
        pn, pn_prev = [int(i) for i in rule.split('|')]

        rules_dct.setdefault(pn, set()).add(pn_prev)

    updates = [[int(i) for i in update.split(',')] for update in updates]

    correct_middle_nums_sum = 0
    for line in updates:
        if is_correct(line, rules_dct):
            middle_num_index = len(line) // 2
            correct_middle_nums_sum += line[middle_num_index]

    # Part 1
    print(correct_middle_nums_sum)
