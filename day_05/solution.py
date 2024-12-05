
def read_and_parse(path: str) -> tuple[list[str], list[str]]:
    with open(path, 'r') as f:
        data = f.read()

    rules, updates = data.split('\n\n')

    rules = rules.split('\n')
    updates = updates.split('\n')

    return rules, updates

if __name__ == '__main__':
    path = 'input.txt'

    rules, updates = read_and_parse(path)

    if not updates[-1]:
        updates = updates[:-1]


    print(rules)
    print(updates)

    rules_dct = {}
    for rule in rules:
        pn, pn_prev = [int(i) for i in rule.split('|')]

        rules_dct.setdefault(pn, set()).add(pn_prev)

    print(rules_dct)

    correct_middle_nums_sum = 0
    for _line in updates:
        line = [int(i) for i in _line.split(',')]

        prev_occurrences = set()
        is_correct = True
        for pn in line:
            if rules_dct.setdefault(pn, set()).intersection(prev_occurrences):
                is_correct = False
                break
            prev_occurrences.add(pn)

        if is_correct:
            middle_num_index = len(line) // 2
            correct_middle_nums_sum += line[middle_num_index]

    # Part 1
    print(correct_middle_nums_sum)



