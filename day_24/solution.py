def parse_gate_description(description: str) -> tuple[str, str, str, str]:
    i1, op, i2, _, out = description.split()
    return i1, op, i2, out


def parse_initial_value(initial_value: str) -> tuple[str, int]:
    k, v = initial_value.split(': ')
    return k, int(v)


def run(values: dict[str, int], gates_descriptions: list[tuple[str, str, str, str]]) -> str:
    remaining = gates_descriptions[:]

    while remaining:
        new_remaining = []
        for gate in remaining:
            if gate[0] in values and gate[2] in values:
                match gate[1]:
                    case 'AND':
                        values[gate[3]] = values[gate[0]] & values[gate[2]]
                    case 'OR':
                        values[gate[3]] = values[gate[0]] | values[gate[2]]
                    case 'XOR':
                        values[gate[3]] = values[gate[0]] ^ values[gate[2]]
            else:
                new_remaining.append(gate)
        remaining = new_remaining

    res = []
    for k, v in sorted(values.items(), reverse=True):
        if k.startswith('z'):
            res.append(str(v))

    return ''.join(res)


def initialize(x: int, y: int) -> dict[str, int]:
    x_str = format(x, 'b').zfill(45)
    y_str = format(y, 'b').zfill(45)

    values = {}

    for index, value in enumerate(reversed(x_str)):
        values[f'x{str(index).zfill(2)}'] = int(value)

    for index, value in enumerate(reversed(y_str)):
        values[f'y{str(index).zfill(2)}'] = int(value)

    return values


def get_number_from_values(values: dict[str, int], number: str = 'z') -> int:
    res = []
    for k, v in sorted(values.items(), reverse=True):
        if k.startswith(number):
            res.append(str(v))
    return int(''.join(res), 2)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    initial_states, gates_descriptions = data.split('\n\n')

    initial_states = initial_states.strip().split('\n')
    gates_descriptions = gates_descriptions.strip().split('\n')

    gates_descriptions = [parse_gate_description(g) for g in gates_descriptions]

    values_initial = {k: v for s in initial_states for k, v in [parse_initial_value(s)]}
    values = values_initial.copy()

    remaining = gates_descriptions[:]

    while remaining:
        new_remaining = []
        for gate in remaining:
            if gate[0] in values and gate[2] in values:
                match gate[1]:
                    case 'AND':
                        values[gate[3]] = values[gate[0]] & values[gate[2]]
                    case 'OR':
                        values[gate[3]] = values[gate[0]] | values[gate[2]]
                    case 'XOR':
                        values[gate[3]] = values[gate[0]] ^ values[gate[2]]
            else:
                new_remaining.append(gate)
        remaining = new_remaining

    res = []
    for k, v in sorted(values.items(), reverse=True):
        if k.startswith('z'):
            res.append(str(v))

    # Part 1
    print(''.join(res))
    print(int(''.join(res), 2))

    _gates_descriptions = gates_descriptions[:]

    swaps = []

    incorrect_bits = []
    x, y = 1, 1
    for i in range(45):
        _values = initialize(x, y)
        result = run(_values, _gates_descriptions)

        if int(result, 2) != x + y:
            for g in _gates_descriptions:
                if g[1] == 'XOR' and not g[3].startswith('z'):
                    if _values[g[3]] == 1:
                        z_gate_to_swap = f'z{(i + 1):02}'
                        swap_candidate = g

                        z_gate = [g for g in _gates_descriptions if g[3] == z_gate_to_swap][0]
                        _gates_descriptions = [g for g in _gates_descriptions if g not in [z_gate, swap_candidate]] + \
                                              [(*z_gate[:-1], swap_candidate[-1]), (*swap_candidate[:-1], z_gate[-1])]

                        # Check if it is fixed
                        _values = initialize(x, y)
                        result = run(_values, _gates_descriptions)

                        swaps.append((z_gate[-1], swap_candidate[-1]))
                        break
            else:
                incorrect_bits.append(i)

        x <<= 1
        y <<= 1

    _x = get_number_from_values(values_initial, 'x')
    _y = get_number_from_values(values_initial, 'y')

    expected = _x + _y

    _values_initial = values_initial.copy()
    result = run(values_initial, _gates_descriptions)

    actual = int(result, 2)

    xored = expected ^ actual
    xored_str = format(xored, 'b')

    leading_zeros = xored_str.count('0')

    _x = f'x{str(leading_zeros).zfill(2)}'
    _y = f'y{str(leading_zeros).zfill(2)}'

    _gates_to_swap = [g for g in _gates_descriptions if g[0] == _x and g[2] == _y or g[0] == _y and g[2] == _x]

    _new_gates = [(*_gates_to_swap[0][:-1], _gates_to_swap[1][-1]), (*_gates_to_swap[1][:-1], _gates_to_swap[0][-1])]

    swaps.append((_gates_to_swap[0][-1], _gates_to_swap[1][-1]))

    # Part 2
    print(','.join(sorted([g for pair in swaps for g in pair])))
