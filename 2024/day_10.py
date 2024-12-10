from collections import defaultdict
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    def int_or_dot(char: str):
        return int(char) if char != '.' else -1
    return [[int_or_dot(char) for char in line] for line in raw.split()]


data = parse_raw(raw)


def part_one(data=data):
    results = dict()
    for zero in find_zeros(data):
        results[zero] = find_reachable_nines_from_trailhead(zero, data)
    return sum(results.values())


def find_reachable_nines_from_trailhead(zero, data) -> int:
    seed = [zero]
    for value in range(1, 10):
        seed = find_neighbors_for_list(seed, value=value, data=data)
        seed = list(set(seed))
    return len(seed)


def build_hiking_tree(zero, data):
    trail_dict = defaultdict(list)
    trail_dict[zero] = [None]
    recursive_find_children(zero, data, trail_dict)
    return trail_dict


def recursive_find_children(node, data, trail_dict):
    children = find_children(node, data)
    for child in children:
        if node not in trail_dict[child]:
            trail_dict[child].append(node)
        recursive_find_children(child, data, trail_dict)


def find_children(node, data):
    return find_neighbors(node, node[1] + 1, data)


def find_zeros(data):
    return [((x, y), 0) for y, row in enumerate(data) for x, char in enumerate(row) if char == 0]


def find_neighbors_for_list(start_list, value, data):
    l = []
    for start in start_list:
        n = find_neighbors(start, value, data)
        l.extend(n)
    return l


def find_neighbors(start, value, data):
    (x, y), _ = start
    neighbor_coordinates = [
        (x, y-1),
        (x+1, y),
        (x, y+1),
        (x-1, y),
    ]
    return [
        (coord, value) for coord in neighbor_coordinates
        if 0 <= coord[0] < len(data[0])
        if 0 <= coord[1] < len(data)
        if data[coord[1]][coord[0]] == value
    ]


def part_two(data=data):
    rating_dict = dict()
    zeros = find_zeros(data)
    for zero in zeros:
        trail_dict = build_hiking_tree(zero, data)
        paths_to_reach_dict = dict()
        for node in trail_dict.keys():
            paths_to_reach_dict[node] = paths_to_reach_for_node(node, trail_dict)
        rating = sum([val for (_, nr), val in paths_to_reach_dict.items() if nr == 9])
        rating_dict[zero] = rating
    return sum(rating_dict.values())


def paths_to_reach_for_node(node, trail_dict):
    if trail_dict[node] == [None]:
        return 1
    return sum(paths_to_reach_for_node(parent, trail_dict) for parent in trail_dict[node])

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
