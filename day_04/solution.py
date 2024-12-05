from collections.abc import Iterable


def is_safe(data: list, i: int, j: int) -> bool:
    len_i = len(data)
    len_j = len(data[0])

    return 0 <= i < len_i and 0 <= j < len_j


def indices_prev(end_index: int, word_len: int) -> Iterable[int]:
    min_j = end_index - word_len + 1
    max_j = end_index + 1
    return range(min_j, max_j)


def indices_next(start_index: int, word_len: int) -> Iterable[int]:
    min_j = start_index
    max_j = start_index + word_len
    return range(min_j, max_j)


def word_right(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _j in indices_next(j, word_len):
        if is_safe(data, i, _j):
            letters.append(data[i][_j])
    return ''.join(letters)


def word_left(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _j in indices_prev(j, word_len):
        if is_safe(data, i, _j):
            letters.append(data[i][_j])
    return ''.join(letters[::-1])


def word_up(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i in indices_prev(i, word_len):
        if is_safe(data, _i, j):
            letters.append(data[_i][j])
    return ''.join((letters[::-1]))


def word_down(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i in indices_next(i, word_len):
        if is_safe(data, _i, j):
            letters.append(data[_i][j])
    return ''.join(letters)


def word_left_up(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i, _j in zip(indices_prev(i, word_len), indices_prev(j, word_len)):
        if is_safe(data, _i, _j):
            letters.append(data[_i][_j])
    return ''.join(letters[::-1])


def word_left_down(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i, _j in zip(reversed(list(indices_next(i, word_len))), indices_prev(j, word_len)):
        if is_safe(data, _i, _j):
            letters.append(data[_i][_j])
    return ''.join(letters[::-1])


def word_right_up(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i, _j in zip(reversed(list(indices_prev(i, word_len))), indices_next(j, word_len)):
        if is_safe(data, _i, _j):
            letters.append(data[_i][_j])
    return ''.join(letters)


def word_right_down(data: list, i: int, j: int, word_len: int) -> str:
    letters = []
    for _i, _j in zip(indices_next(i, word_len), indices_next(j, word_len)):
        if is_safe(data, _i, _j):
            letters.append(data[_i][_j])
    return ''.join(letters)


def get_words(data: list, i: int, j: int, word_len: int = 4) -> list[str]:
    return [
        word_right(data, i, j, word_len),
        word_left(data, i, j, word_len),
        word_up(data, i, j, word_len),
        word_down(data, i, j, word_len),
        word_left_up(data, i, j, word_len),
        word_left_down(data, i, j, word_len),
        word_right_up(data, i, j, word_len),
        word_right_down(data, i, j, word_len)
    ]


def is_x_mas(data: list, i, j):
    len_i = len(data)
    len_j = len(data[0])
    # This ensures the indices are "safe"
    if not (0 < i < len_i - 1) or not (0 < j < len_j - 1):
        return False

    w1 = data[i - 1][j - 1] + data[i][j] + data[i + 1][j + 1]
    w2 = data[i + 1][j - 1] + data[i][j] + data[i - 1][j + 1]

    w1 = ''.join(w1)
    w2 = ''.join(w2)

    w1_ok = w1 == 'MAS' or w1[::-1] == 'MAS'
    w2_ok = w2 == 'MAS' or w2[::-1] == 'MAS'

    return w1_ok and w2_ok


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = f.readlines()

    data = [l.strip() for l in data]

    n_rows = len(data)
    n_cols = len(data[0])

    total = 0
    for i in range(n_rows):
        for j in range(n_cols):
            if data[i][j] == 'X':
                words = get_words(data, i, j)
                for w in words:
                    if w == 'XMAS':
                        total += 1

    # Part 1
    print(total)

    total = 0
    for i in range(n_rows):
        for j in range(n_cols):
            if data[i][j] == 'A':
                if is_x_mas(data, i, j):
                    total += 1

    # Part 2
    print(total)
