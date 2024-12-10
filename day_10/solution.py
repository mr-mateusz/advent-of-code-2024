def neighbours(data: list[list], r: int, c: int) -> list[tuple[int, int]]:
    possible_neighbours = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    neighbours = [n for n in possible_neighbours if 0 <= n[0] < len(data) and 0 <= n[1] < len(data[0])]
    return neighbours


def find_unique_trails(data: list[list], start_r: int, start_c: int) -> int:
    to_check = [(start_r, start_c)]

    peaks_found = set()
    while to_check:
        r, c = to_check.pop(0)
        current_val = data[r][c]

        if current_val == 9:
            peaks_found.add((r, c))
        else:
            for n in neighbours(data, r, c):
                if data[n[0]][n[1]] == current_val + 1:
                    to_check.append(n)

    return len(peaks_found)


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = [r.strip() for r in f.readlines()]

    data = [[int(v) for v in l] for l in data]

    total_score = 0
    for r in range(len(data)):
        for c in range(len(data[0])):
            if data[r][c] == 0:
                total_score += find_unique_trails(data, r, c)

    print(total_score)
