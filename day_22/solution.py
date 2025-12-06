from collections import deque, defaultdict


def mix(number: int, value: int) -> int:
    return number ^ value


def prune(number: int) -> int:
    return number % 16777216


def next_secret_number(number: int) -> int:
    value = number * 64
    secret_number = mix(number, value)
    secret_number = prune(secret_number)

    value = secret_number // 32
    secret_number = mix(secret_number, value)
    secret_number = prune(secret_number)

    value = secret_number * 2048
    secret_number = mix(secret_number, value)
    secret_number = prune(secret_number)

    return secret_number


def n_th_secret_number(number: int, n: int) -> int:
    for _ in range(n):
        number = next_secret_number(number)
    return number


def map_sequences_to_bananas(number: int, n: int) -> dict[tuple, int]:
    last_four_changes = deque(maxlen=4)
    mapping = {}

    prev_last_digit = number % 10
    for _ in range(n):
        number = next_secret_number(number)
        number_last_digit = number % 10
        change = number_last_digit - prev_last_digit

        last_four_changes.append(change)
        # add only the first occurrence of a sequence
        if len(last_four_changes) == 4 and tuple(last_four_changes) not in mapping:
            mapping[tuple(last_four_changes)] = number_last_digit
        prev_last_digit = number_last_digit

    return mapping


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as file:
        data = [int(l.strip()) for l in file]

    # which secret number to generate
    n = 2000

    n_th_secret_numbers = [n_th_secret_number(initial_secret_number, n) for initial_secret_number in data]

    # Part 1
    print(sum(n_th_secret_numbers))

    final_mapping = defaultdict(int)
    for initial_secret_number in data:
        mapping = map_sequences_to_bananas(initial_secret_number, n)
        for change_seq, value in mapping.items():
            final_mapping[change_seq] += value

    # Part 2
    print(sorted(final_mapping.items(), key=lambda x: x[1], reverse=True)[0][1])
