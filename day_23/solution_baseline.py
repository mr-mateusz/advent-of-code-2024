from collections import defaultdict
from typing import Mapping

from tqdm import tqdm


def create_neighbours_dct(lines: list[str]) -> dict[str, set[str]]:
    neighbours_dct = defaultdict(set)
    for l in lines:
        node_a, node_b = l.split('-')

        neighbours_dct[node_a].add(node_b)
        neighbours_dct[node_b].add(node_a)

    return neighbours_dct


def find_3_cliques(neighbours_dct: Mapping[str, set[str]]) -> set[frozenset[str]]:
    cliques = set()

    nodes = neighbours_dct.keys()
    for initial_node in nodes:
        neighbours = neighbours_dct[initial_node]
        for neighbour in neighbours:
            second_level_neighbours = neighbours_dct[neighbour]
            for second_level_neighbour in second_level_neighbours:
                if initial_node in neighbours_dct[second_level_neighbour]:
                    cliques.add(frozenset([initial_node, neighbour, second_level_neighbour]))
    return cliques


def expand_clique(current_clique: set, neighbours_dct: Mapping[str, set[str]]) -> set[str]:
    remaining_nodes = set(neighbours_dct.keys()) - current_clique

    biggest_clique = current_clique
    for rn in remaining_nodes:
        rn_neighbours = neighbours_dct[rn]

        if not current_clique - rn_neighbours:
            expanded = expand_clique(current_clique | {rn}, neighbours_dct)
            if len(expanded) > len(biggest_clique):
                biggest_clique = expanded
    return biggest_clique


def find_biggest_clique(neighbours_dct: Mapping[str, set[str]]) -> set[str]:
    nodes = neighbours_dct.keys()

    current_biggest_clique = set()
    for node in tqdm(nodes):
        clique = expand_clique({node}, neighbours_dct)
        if len(clique) > len(current_biggest_clique):
            current_biggest_clique = clique
    return current_biggest_clique


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as file:
        data = [l.strip() for l in file]

    neighbours_dct = create_neighbours_dct(data)

    cliques = find_3_cliques(neighbours_dct)

    cliques_filtered = [c for c in cliques if any(n.startswith('t') for n in c)]

    # Part 1
    print(len(cliques_filtered))

    # part 2
    clique = find_biggest_clique(neighbours_dct)

    print(','.join(sorted(clique)))
