if __name__ == "__main__":
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.readlines()

    data = [d.strip().split() for d in data]
    l1, l2 = list(zip(*data))
    
    l1 = [int(n) for n in l1]
    l2 = [int(n) for n in l2]

    diffs = [n1 - n2 if n1 > n2 else n2 - n1 for n1, n2 in zip(sorted(l1), sorted(l2))]
    
    # Part 1
    print(sum(diffs))

    l2_counts = {}

    for n in l2:
        try:
            l2_counts[n] += 1
        except KeyError:
            l2_counts[n] = 1

    total = 0
    for n in l1:
        try:
            score =n * l2_counts[n]
        except KeyError:
            score = 0
        total += score

    # Part 2
    print(total)
