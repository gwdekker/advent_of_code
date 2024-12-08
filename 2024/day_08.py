from collections import defaultdict
from enum import StrEnum, auto
from itertools import combinations, count

import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


class CalculationMode(StrEnum):
    simple = auto()
    add_resonance = auto()


def parse_raw(raw: str):
    locations = defaultdict(list)
    mx = raw.split()
    for y, row in enumerate(mx):
        for x, cell in enumerate(row):
            if cell == ".":
                continue
            locations[cell].append((x, y))
    max_xy = (len(mx[0]), len(mx))
    return locations, max_xy


def distance(a, b):
    return (b[0] - a[0]), (b[1] - a[1])


def antinode_positions_for_pair(a, b, max_xy, mode: CalculationMode):
    d = distance(a, b)
    if mode == CalculationMode.simple:
        pos1 = a[0] - d[0], a[1] - d[1]
        pos2 = b[0] + d[0], b[1] + d[1]
        return [
            pos for pos in (pos1, pos2)
            if pos_in_bounds(pos, max_xy)
        ]
    if mode == CalculationMode.add_resonance:
        positions = []
        for i in count(1):
            pos1 = a[0] - d[0]*i, a[1] - d[1]*i
            if not pos_in_bounds(pos1, max_xy):
                break
            positions.append(pos1)
        for i in count(1):
            pos2 = b[0] + d[0]*i, b[1] + d[1]*i
            if not pos_in_bounds(pos2, max_xy):
                break
            positions.append(pos2)
        return positions


def pos_in_bounds(pos, max_xy):
    return 0 <= pos[0] < max_xy[0] and 0 <= pos[1] < max_xy[1]


def find_antinode_positions(locations, max_xy, mode: CalculationMode):
    antinode_positions = defaultdict(list)
    for freq, antennae_for_frequency in locations.items():
        for pair in combinations(antennae_for_frequency, 2):
            antinode_positions[freq].extend(antinode_positions_for_pair(*pair, max_xy, mode))
    return antinode_positions


def nr_unique_positions_in_dict(positions_dict):
    return len(set(
        pos
        for freq, positions in positions_dict.items()
        for pos in positions
    ))

data = parse_raw(raw)


def part_one(data=data):
    locations, max_xy = data
    antinode_positions = find_antinode_positions(locations, max_xy, CalculationMode.simple)
    return nr_unique_positions_in_dict(antinode_positions)


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    locations, max_xy = data
    antinode_positions = find_antinode_positions(locations, max_xy, CalculationMode.add_resonance)
    antinodes_and_antennae = {
        freq: locations.get(freq, []) + antinode_positions.get(freq, [])
        for freq in set(locations) | set(antinode_positions)
    }
    return nr_unique_positions_in_dict(antinodes_and_antennae)

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
