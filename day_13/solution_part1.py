import numpy as np
import pulp


def extract_numbers_button(line: str) -> tuple[int, int]:
    splitted = line.split('+')
    x = int(splitted[1][:-3])
    y = int(splitted[2])

    return x, y


def extract_numbers_prize(line: str) -> tuple[int, int]:
    splitted = line.split('=')
    x = int(splitted[1][:-3])
    y = int(splitted[2])

    return x, y


def parse_equations(example: str) -> tuple[np.ndarray, np.ndarray]:
    lines = example.split('\n')
    x1, y1 = extract_numbers_button(lines[0])
    x2, y2 = extract_numbers_button(lines[1])

    b1, b2 = extract_numbers_prize(lines[2])

    a = np.array([[x1, x2], [y1, y2]])
    b = np.array([b1, b2])
    return a, b


def solve(a: np.ndarray, b: np.ndarray) -> int | None:
    problem = pulp.LpProblem("", sense=pulp.LpMinimize)

    n_A = pulp.LpVariable("n_A", lowBound=0, upBound=100, cat=pulp.LpInteger)
    n_B = pulp.LpVariable("n_B", lowBound=0, upBound=100, cat=pulp.LpInteger)

    problem += 3 * n_A + 1 * n_B, "Total Cost"

    problem += a[0, 0] * n_A + a[0, 1] * n_B == b[0], "Constraint1"
    problem += a[1, 0] * n_A + a[1, 1] * n_B == b[1], "Constraint2"

    problem.solve()

    if problem.status == 1:
        return pulp.value(3 * n_A + 1 * n_B)
    else:
        return 0


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read().strip()

    examples = data.split('\n\n')

    total = 0
    for e in examples:
        a, b = parse_equations(e)

        total += solve(a, b)

    # Part 1
    print(total)
