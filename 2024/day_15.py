from enum import StrEnum, auto
from pathlib import Path
from typing import Literal

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
#
# raw = """
# ##########
# #..O..O.O#
# #......O.#
# #.OO..O.O#
# #..O@..O.#
# #O#..O...#
# #O..O..O.#
# #.OO.O.OO#
# #....O...#
# ##########
#
# <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
# vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
# ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
# <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
# ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
# ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
# >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
# <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
# ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
# v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
# """
#



class Things(StrEnum):
    robot = "@"
    empty = "."
    box = "O"
    wall = "#"
    left_box = "["
    right_box = "]"


def parse_raw(raw: str):
    grid, directions = raw.split("\n\n")
    grid = [[Things(char) for char in string] for string in grid.split()]
    directions = [c for c in directions if c != "\n"]
    return grid, directions

def resize_grid(grid):
    new_grid = []
    for line in grid:
        new_line = []
        for thing in line:
            match thing:
                case Things.wall:
                    new_line.extend([Things.wall, Things.wall])
                case Things.box:
                    new_line.extend([Things.left_box, Things.right_box])
                case Things.empty:
                    new_line.extend([Things.empty, Things.empty])
                case Things.robot:
                    new_line.extend([Things.robot, Things.empty])
                case _:
                    raise ValueError
        new_grid.append(new_line)
    return new_grid



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
            if t in {Things.box, Things.left_box}:
                gps += 100*y + x
    return gps

def print_grid(grid):
    for line in grid:
        print("".join(t.value for t in line))
        # for thing in line:
        #     print(thing.value, sep="")
    print("")



# aoc_helper.lazy_test(day=daygcc, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    grid, directions = data
    grid = resize_grid(grid)
    print_grid(grid)
    while directions:
        robot_coords = find_robot(grid)
        direction = directions.pop(0)
        print(direction)
        list_with_robot = filter_from_grid(grid, direction, robot_coords)
        if direction in {'<', '>'}:
            new_list = move_a_list(list_with_robot)
            grid = put_list_in_grid(new_list, robot_coords, direction, grid)
        else:
            l_things = list_with_robot
            if l_things[-1] != Things.wall:
                raise ValueError
            elif l_things[0] != Things.robot:
                raise ValueError
            elif l_things.count(Things.wall) != 1:
                raise ValueError
            elif Things.empty not in l_things:
                continue
            elif l_things[1] == Things.empty:
                new_list = move_a_list(list_with_robot)
                grid = put_list_in_grid(new_list, robot_coords, direction, grid)
            elif l_things[1] in {Things.left_box, Things.right_box}:
                coord = above(robot_coords) if direction == "^" else below(robot_coords)
                can_push, coords = can_push_box_up_down(coord, grid, direction)
                if can_push:
                    new_list = move_a_list(list_with_robot)
                    grid = put_list_in_grid(new_list, robot_coords, direction, grid)
                    additional_coords_to_push = [c for c in coords if c[0] != robot_coords[0]]
                    reverse = False if direction == "^" else True
                    additional_coords_to_push = sorted(additional_coords_to_push , key=lambda coord: coord[1], reverse=reverse)
                    grid_copy = grid.copy()
                    for ac in additional_coords_to_push:
                        new_coord = above(ac) if direction == "^" else below(ac)
                        grid[new_coord[1]][new_coord[0]] = grid_copy[ac[1]][ac[0]]
                        grid[ac[1]][ac[0]] = Things.empty
                else:
                    continue
            else:
                raise ValueError
        print_grid(grid)
    return gps_for_full_grid(grid)


def can_push_box_up_down(coord, grid, direction_to_push: Literal["^", "v"]):
    contents = grid[coord[1]][coord[0]]
    if contents == Things.left_box:
        left_box_coord = coord
        right_box_coord = right_from(left_box_coord)
    elif contents == Things.right_box:
        right_box_coord = coord
        left_box_coord = left_from(right_box_coord)
    elif contents == Things.empty:
        return True, [(None, None)]
    else:
        raise ValueError

    coords_to_push_to = (
        (above(left_box_coord), above(right_box_coord))
        if direction_to_push == "^"
        else (below(left_box_coord), below(right_box_coord))
    )
    contents_of_coords_to_push_to = (
        grid[coords_to_push_to[0][1]][coords_to_push_to[0][0]],
        grid[coords_to_push_to[1][1]][coords_to_push_to[1][0]],
    )

    if all([c == Things.empty for c in contents_of_coords_to_push_to]):
        return True, [left_box_coord, right_box_coord]
    elif any([c == Things.wall for c in contents_of_coords_to_push_to]):
        return False, [left_box_coord, right_box_coord]
    else:
        b = [can_push_box_up_down(c, grid, direction_to_push) for c in coords_to_push_to]
        bools = [bl for (bl, _) in b]
        coords = [
            x
            for (_, coords) in b
            for x in [left_box_coord, right_box_coord, *coords]
            if x is not (None, None)
        ]
        return all(bools), list(set(coords))


def above(coord):
    return coord[0], coord[1] - 1

def below(coord):
    return coord[0], coord[1] + 1

def right_from(coord):
    return coord[0] + 1, coord[1]

def left_from(coord):
    return coord[0] - 1, coord[1]

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
