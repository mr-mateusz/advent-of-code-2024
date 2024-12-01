

if __name__ == "__main__":
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.readlines()

    data = [d.strip().split() for d in data]
    l1, l2 = list(zip(*data))
    
    l1 = [int(n) for n in l1]
    l2 = [int(n) for n in l2]
    
    l1 = sorted(l1)
    l2 = sorted(l2)

    diffs = [n1 - n2 if n1 > n2 else n2 - n1 for n1, n2 in zip(l1, l2)]
    
    # Part 1
    print(sum(diffs))
