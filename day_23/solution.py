from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import cache
from typing import Mapping


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


def expand_clique(current_clique: set[str], neighbours_dct: Mapping[str, set[str]],
                  nodes_to_consider: frozenset[str]) -> set[str]:
    @cache
    def _expand_clique(current_clique: frozenset[str], nodes_to_consider: frozenset[str]) -> set[str]:
        current_clique = set(current_clique)
        remaining_nodes = set(nodes_to_consider) - current_clique

        biggest_clique = current_clique
        for rn in remaining_nodes:
            rn_neighbours = neighbours_dct[rn]

            if not current_clique - rn_neighbours:
                expanded = expand_clique(current_clique | {rn}, neighbours_dct, nodes_to_consider)
                if len(expanded) > len(biggest_clique):
                    biggest_clique = expanded
        return biggest_clique

    return _expand_clique(frozenset(current_clique), nodes_to_consider)


def find_biggest_clique(neighbours_dct: Mapping[str, set[str]], nodes_to_consider: frozenset[str]) -> set[str]:
    nodes = nodes_to_consider

    current_biggest_clique = set()
    for node in nodes:
        clique = expand_clique({node}, neighbours_dct, nodes_to_consider)
        if len(clique) > len(current_biggest_clique):
            current_biggest_clique = clique
    return current_biggest_clique


def find_biggest_clique_task(cliques: list[set[str]], neighbours_dct: Mapping[str, set[str]]) -> set[str]:
    biggest_clique = set()
    for i, clique in enumerate(cliques):
        print(i + 1, len(cliques))
        considered_nodes = set(neighbours_dct.keys())
        for n in clique:
            considered_nodes = frozenset(considered_nodes.intersection(neighbours_dct[n]))
        biggest_clique_in_subset = find_biggest_clique(neighbours_dct, considered_nodes)
        biggest_clique_in_subset = biggest_clique_in_subset.union(clique)
        if len(biggest_clique_in_subset) > len(biggest_clique):
            biggest_clique = biggest_clique_in_subset
    return biggest_clique


def find_biggest_clique_multiprocessing(cliques: list[set[str]], neighbours_dct: Mapping[str, set[str]]) -> set[str]:
    num_workers = 15
    chunk_size = len(cliques) // num_workers

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(0, len(cliques), chunk_size):
            chunk = cliques[i:i + chunk_size]
            futures.append(executor.submit(find_biggest_clique_task, chunk, neighbours_dct))

        results = []
        for future in as_completed(futures):
            results.append(future.result())

    # Combine results to find the largest clique
    biggest_clique = set()
    for result in results:
        if len(result) > len(biggest_clique):
            biggest_clique = result

    return biggest_clique


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as file:
        data = [l.strip() for l in file]

    neighbours_dct = create_neighbours_dct(data)

    cliques = find_3_cliques(neighbours_dct)

    cliques_filtered = [c for c in cliques if any(n.startswith('t') for n in c)]

    # Part 1
    print(len(cliques_filtered))

    clique = find_biggest_clique_multiprocessing(list(cliques), neighbours_dct)

    # Part 2
    print(','.join(sorted(clique)))
