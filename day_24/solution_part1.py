def parse_gate_description(description: str) -> tuple[str, str, str, str]:
    i1, op, i2, _, out = description.split()
    return i1, op, i2, out


def parse_initial_value(initial_value: str) -> tuple[str, int]:
    k, v = initial_value.split(': ')
    return k, int(v)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    initial_states, gates_descriptions = data.split('\n\n')

    initial_states = initial_states.strip().split('\n')
    gates_descriptions = gates_descriptions.strip().split('\n')

    gates_descriptions = [parse_gate_description(g) for g in gates_descriptions]

    values = {k: v for s in initial_states for k, v in [parse_initial_value(s)]}

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
