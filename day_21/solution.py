from collections import deque
from functools import cache


def complexity(code: str, seq_len: int) -> int:
    code_value = int(code.strip('A'))
    return code_value * seq_len


@cache
def generate_shortest_paths(start_pos, end_pos):
    if start_pos == end_pos:
        return [[start_pos]]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start_pos, [start_pos])])
    shortest_paths = []
    min_length = float('inf')

    while queue:
        (x, y), path = queue.popleft()

        if len(path) > min_length:
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) == end_pos:
                new_path = path + [(nx, ny)]
                if len(new_path) < min_length:
                    min_length = len(new_path)
                    shortest_paths = [new_path]
                elif len(new_path) == min_length:
                    shortest_paths.append(new_path)
            elif 0 <= nx and 0 <= ny:
                queue.append(((nx, ny), path + [(nx, ny)]))

    return shortest_paths


def path_to_moves(path):
    moves = []
    for i in range(1, len(path)):
        prev_x, prev_y = path[i - 1]
        curr_x, curr_y = path[i]

        if curr_x == prev_x + 1 and curr_y == prev_y:
            moves.append('v')
        elif curr_x == prev_x and curr_y == prev_y + 1:
            moves.append('>')
        elif curr_x == prev_x and curr_y == prev_y - 1:
            moves.append('<')
        elif curr_x == prev_x - 1 and curr_y == prev_y:
            moves.append('^')

    return ''.join(moves)


@cache
def numeric_mappings(start_pos, end_pos, type='n'):
    if type == 'n':
        positions = [
            '789',
            '456',
            '123',
            '#0A'
        ]
    else:
        positions = [
            '#^A',
            '<v>'
        ]
    banned_position = '#'

    start_pos_index = [(i, row.index(start_pos)) for i, row in enumerate(positions) if start_pos in row][0]
    end_pos_index = [(i, row.index(end_pos)) for i, row in enumerate(positions) if end_pos in row][0]

    banned_position_indices = [(i, row.index(banned_position)) for i, row in enumerate(positions) if
                               banned_position in row]

    all_paths = generate_shortest_paths(start_pos_index, end_pos_index)

    filtered_paths = []
    for path in all_paths:
        if not any(pos in banned_position_indices for pos in path):
            filtered_paths.append(path)

    moves = [path_to_moves(path) for path in filtered_paths]

    moves = [m + 'A' for m in moves]

    return moves


@cache
def map_sequence(seq: str, start_pos: str = 'A', type: str = 'n') -> list[str]:
    from_pos = start_pos

    combinations = []
    for to_pos in seq:
        possible_mappings = numeric_mappings(from_pos, to_pos, type)
        if not combinations:
            combinations = possible_mappings
        else:
            new_combinations = []
            for c in combinations:
                for p in possible_mappings:
                    new_combinations.append(c + p)
            combinations = new_combinations
        from_pos = to_pos

    return combinations


@cache
def translate_moves(seq: str, start_pos: str = 'A', depth: int = 1) -> int:
    translated = map_sequence(seq, start_pos, type='d')

    if depth == 1:
        return min(len(t) for t in translated)

    nested_translated = []
    for sequence in translated:
        # split sequence into sub-sequences on each A
        nested_translated_for_sequence_lens = []
        sequences = [s + 'A' for s in sequence.split('A')][:-1]
        for s in sequences:
            nested_translated_for_sequence_lens.append(translate_moves(s, start_pos, depth - 1))
        nested_translated.append(sum(nested_translated_for_sequence_lens))

    return min(nested_translated)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [l.strip() for l in f]

    depth = 2

    total = 0
    for line in data[:]:
        translated_initial = map_sequence(line, 'A', 'n')

        final_sequences = []
        for t in translated_initial:
            final_sequences.append(translate_moves(t, 'A', depth))

        shortest_sequence = min(final_sequences)

        total += complexity(line, shortest_sequence)

    # Part 1
    print(total)

    depth = 25

    total = 0
    for line in data[:]:
        translated_initial = map_sequence(line, 'A', 'n')

        final_sequences = []
        for t in translated_initial:
            final_sequences.append(translate_moves(t, 'A', depth))

        shortest_sequence = min(final_sequences)

        total += complexity(line, shortest_sequence)

    # Part 2
    print(total)