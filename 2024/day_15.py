from enum import StrEnum, auto
from pathlib import Path
import aoc_helper

year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)
# raw = """
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########
#
# <^^>>>vv<v>>v<<
# """

class Things(StrEnum):
    robot = "@"
    empty = "."
    box = "O"
    wall = "#"


def parse_raw(raw: str):
    grid, directions = raw.split("\n\n")
    grid = [[Things(char) for char in string] for string in grid.split()]
    directions = [c for c in directions if c != "\n"]
    return grid, directions


data = parse_raw(raw)


def part_one(data=data):
    grid, directions = data

    while directions:
        robot_coords = find_robot(grid)
        direction = directions.pop(0)
        list_with_robot = filter_from_grid(grid, direction, robot_coords)
        new_list = move_a_list(list_with_robot)
        grid = put_list_in_grid(new_list, robot_coords, direction, grid)
    return gps_for_full_grid(grid)


def find_robot(grid):
    for y, row in enumerate(grid):
        if Things.robot in row:
            for x, char in enumerate(row):
                if char == Things.robot:
                    return x, y
    raise ValueError("robot not found")


def filter_from_grid(grid, direction, coords):
    x, y = coords
    match direction:
        case ">":
            row = grid[y][x:]
        case "<":
            row = list(reversed(grid[y][:x+1]))
        case "^":
            row = list(reversed([grid[i][x] for i in range(0, y+1)]))
        case "v":
            row = [grid[i][x] for i in range(y, len(grid))]
        case _:
            raise ValueError
    assert row[0] == Things.robot
    assert row[-1] == Things.wall
    return [t for idx, t in enumerate(row) if idx <= row.index(Things.wall)]


def put_list_in_grid(a_list, start_position, direction, grid):
    x, y = start_position
    match direction:
        case ">":
            for i, elm in enumerate(a_list):
                grid[y][x+i] = elm
        case "<":
            for i, elm in enumerate(a_list):
                grid[y][x - i] = elm
        case "^":
            for i, elm in enumerate(a_list):
                grid[y-i][x] = elm
        case "v":
            for i, elm in enumerate(a_list):
                grid[y+i][x] = elm
        case _:
            raise ValueError
    return grid


def move_a_list(l_things: list[Things]) -> list[Things]:
    if l_things[-1] != Things.wall:
        raise ValueError
    if l_things[0] != Things.robot:
        raise ValueError
    if l_things.count(Things.wall) != 1:
        raise ValueError
    if Things.empty in l_things:
        l_things.remove(Things.empty)
        l_things.insert(0, Things.empty)
    return l_things

def gps_for_full_grid(grid):
    gps = 0
    for y, row in enumerate(grid):
        for x, t in enumerate(row):
            if t == Things.box:
                gps += 100*y + x
    return gps





# aoc_helper.lazy_test(day=daygcc, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass


# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
