from collections import Counter
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

# raw = aoc_helper.fetch(day, year)
raw = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

def parse_raw(raw: str):
    track_tiles = set()
    wall_tiles = set()
    for y, line in enumerate(raw.splitlines()):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
                track_tiles.add(start)
            if char == "E":
                end = (x, y)
                track_tiles.add(end)
            if char == "#":
                wall_tiles.add((x, y))
            if char == ".":
                track_tiles.add((x, y))
    return start, end, track_tiles, wall_tiles


data = parse_raw(raw)


def part_one(data=data):
    start, end, track_tiles, wall_tiles = data
    track_dict = create_track_dict(end, start, track_tiles)
    cheats = []
    for coord, score in track_dict.items():
        cheats.extend( find_cheats(coord, score, wall_tiles, track_dict))
    counted = Counter(c[2] for c in cheats)
    return sum([v for k, v in counted.items() if k >= 100])


def find_cheats(coord, score, wall_tiles, track_dict):
    x, y = coord
    wall_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    track_moves = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
    cheats = []
    for cheat_candidate in zip(wall_moves, track_moves):
        wall, track = cheat_candidate
        if wall not in wall_tiles:
            continue
        if track not in track_dict:
            continue
        if track_dict[track] > score:
            continue
        cheats.append((track, coord, score - track_dict[track] - 2))
    return cheats


    return candidates[0]


def create_track_dict(end, start, track_tiles):
    track_dict = {start: 0}
    this_tile = start
    while True:
        track_tiles.remove(this_tile)
        next_tile = next_track_tile(this_tile, track_tiles)
        track_dict[next_tile] = track_dict[this_tile] + 1
        this_tile = next_tile
        if this_tile == end:
            assert len(track_tiles) == 1
            return track_dict


def next_track_tile(track_tile, track_tiles):
    x, y = track_tile
    moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    candidates = [
        move for move in moves
        if move in track_tiles
    ]
    if len(candidates) != 1:
        raise ValueError(f"Expected 1 candidate, got {len(candidates)}")
    return candidates[0]

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    # prob turn it around: rather calc the path, then check for each point where the diff is at least 50(100) if the
    # manhattan distance is less than 20
    start, end, track_tiles, wall_tiles = data
    track_dict = create_track_dict(end, start, track_tiles)
    cheats = []
    for coord0, score0 in track_dict.items():
        for coord1, score1 in track_dict.items():
            if score1 - score0 >= 50:
                if manhattan(coord0, coord1) <= 20:
                    cheats.append((coord0, coord1, score1 - score0))
    counted = Counter(c[2] for c in cheats)
    return sum([v for k, v in counted.items() if k >= 100])

    pass

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
