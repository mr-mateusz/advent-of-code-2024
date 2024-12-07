def is_ok(line: tuple[int, list[int]], try_concat: bool = False) -> bool:
    """Input tuple: (expected_result, [values])"""
    stack = [line]

    while stack:
        to_check = stack.pop()
        expected, values = to_check

        if len(values) > 1:
            fv, sv = values[0], values[1]
            if fv <= expected:
                # If values are equal we still check in case of 0 (for addiction) and 1 (for multiplication)
                stack.append((expected, [fv + sv] + values[2:]))
                stack.append((expected, [fv * sv] + values[2:]))
                if try_concat:
                    stack.append((expected, [int(str(fv) + str(sv))] + values[2:]))
            if fv > expected:
                # The value is already too big, we don't check further in this "branch"
                pass
        if len(values) == 1:
            fv = values[0]
            if fv == expected:
                return True
    return False


if __name__ == '__main__':
    path = "input.txt"

    with open(path, 'r') as f:
        data = [l.strip() for l in f.readlines()]

    data = [l.split(': ') for l in data]
    data = [(int(res), [int(v) for v in vals.split()]) for res, vals in data]

    total = 0
    for line in data:
        if is_ok(line):
            total += line[0]

    # Part 1
    print(total)

    total = 0
    for line in data:
        if is_ok(line, try_concat=True):
            total += line[0]

    # Part 2
    print(total)