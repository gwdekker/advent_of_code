from collections import defaultdict
from enum import StrEnum, auto
from itertools import combinations, count
from pathlib import Path

import aoc_helper

year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])


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
        for i in count():  # include 0 to include the antennae locations
            pos1 = a[0] - d[0]*i, a[1] - d[1]*i
            if not pos_in_bounds(pos1, max_xy):
                break
            positions.append(pos1)
        for i in count():
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


def part_one(data):
    antinode_positions = find_antinode_positions(*data, CalculationMode.simple)
    return nr_unique_positions_in_dict(antinode_positions)

def part_two(data):
    antinode_positions = find_antinode_positions(*data, CalculationMode.add_resonance)
    return nr_unique_positions_in_dict(antinode_positions)


raw = aoc_helper.fetch(day, year)
data = parse_raw(raw)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
