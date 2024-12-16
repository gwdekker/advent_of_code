from collections import deque
from enum import StrEnum
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

import sys
sys.setrecursionlimit(10_000)

# raw = """
# ###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############
# """
# raw = """
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################
# """

class Things(StrEnum):
    start = "S"
    end = "E"
    empty = "."
    wall = "#"


class Facing(StrEnum):
    north = "^"
    east = ">"
    south = "v"
    west = "<"



def parse_raw(raw: str):
    return [[Things(char) for char in string] for string in raw.split()]


data = parse_raw(raw)

def find_start_or_end(grid, what):
    for y, row in enumerate(grid):
        if what in row:
            for x, char in enumerate(row):
                if char == what:
                    return x, y
    raise ValueError(f"{what} not found")

def part_one(data=data):
    draw_grid(data)
    empties = initialize_empties(grid=data)
    positions = {key: None for key in empties}
    start_position = find_start_or_end(data, Things.start), Facing.east
    start_score = 0
    queue = deque()
    queue.append((start_position, start_score))
    positions[start_position] = start_score
    while queue:
        position, score = queue.popleft()
        candidates = (
            (rotate(position, clockwise=True), score + 1_000),
            (rotate(position, clockwise=False), score + 1_000),
            (move(position), score + 1),
        )
        for cand_pos, cand_score in candidates:
            if cand_pos not in positions:
                # outside of grid
                continue
            if positions[cand_pos] is None:
                # first time we are here
                positions[cand_pos] = cand_score
                queue.append((cand_pos, cand_score))
            elif cand_score < positions[cand_pos]:
                # better route
                positions[cand_pos] = cand_score
                queue.append((cand_pos, cand_score))
            else:  # worse route
                continue
    end_pos = find_start_or_end(grid=data, what=Things.end)
    return min([v for k, v in positions.items() if k[0] == end_pos])



def initialize_empties(grid):
    empties = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if grid[y][x] in {Things.start, Things.end, Things.empty}:
                for direction in Facing:
                    empties.append(((x, y), direction))
    return empties
    raise ValueError("start not found")



def draw_grid(grid):
    for line in grid:
        print("".join(t.value for t in line))
    print("")

def rotate(position, clockwise: bool):
    (x, y), direction = position
    match direction:
        case Facing.north:
            new_direction = Facing.east if clockwise else Facing.west
        case Facing.east:
            new_direction = Facing.south if clockwise else Facing.north
        case Facing.south:
            new_direction = Facing.west if clockwise else Facing.east
        case Facing.west:
            new_direction = Facing.north if clockwise else Facing.south
        case _:
            raise ValueError
    return (x, y), new_direction

def move(position):
    (x, y), direction = position
    match direction:
        case Facing.north:
            return (x, y-1), direction
        case Facing.south:
            return (x, y + 1), direction
        case Facing.east:
            return (x + 1, y), direction
        case Facing.west:
            return (x - 1, y), direction

def get_at(position, grid):
    (x, y), _ = position
    try:
        return grid[y][x]
    except IndexError:
        return None





aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
