from enum import StrEnum, auto

import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    return raw.split()

data = parse_raw(raw)

class Direction(StrEnum):
    up = auto()
    down = auto()
    right = auto()
    left = auto()

class OutOfBoundsError(Exception):
    pass

def turn_right(position):
    x, y, direction = position
    match direction:
        case Direction.up:
            new_direction = Direction.right
        case Direction.right:
            new_direction = Direction.down
        case Direction.down:
            new_direction = Direction.left
        case Direction.left:
            new_direction = Direction.up
        case _:
            raise ValueError()
    return x, y, new_direction

def next_position(position):
    x, y, direction = position
    match direction:
        case Direction.up:
            return x, y-1, direction
        case Direction.right:
            return x+1, y, direction
        case Direction.down:
            return x, y+1, direction
        case Direction.left:
            return x-1, y, direction
        case _:
            raise ValueError()

def part_one(data=data):
    x, y = find_start(data)
    position = x, y, Direction.up
    player_trace = run_from_here(data, position)
    if player_trace is None:
        raise ValueError()
    return len(set((x, y) for x, y, _ in player_trace))

def run_from_here(data, position):
    player_trace = []
    try:
        while True:
            player_trace.append(position)
            maybe_nxt = next_position(position)
            if is_occupied(data, maybe_nxt):
                position = turn_right(position)
            else:
                position = maybe_nxt
            if is_in_loop(position, player_trace):
                return None
    except  OutOfBoundsError:
        return player_trace

def is_in_loop(position, player_trace):
    return position in player_trace

def is_occupied(data, position):
    x, y, _ = position
    if (x < 0) or (y<0):
        raise OutOfBoundsError
    try:
        what = data[y][x]
    except IndexError:
        raise OutOfBoundsError
    if what == "#":
        return True
    elif what == ".":
        return False
    elif what == "^":
        # Crossing over the starting position
        return False
    else:
        raise ValueError

def find_start(data):
    player_token = "^"
    for y, line in enumerate(data):
        if player_token not in line:
            continue
        x = line.index(player_token)
        return x, y

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    # try obstacles at any positions of the orignal path. if not on the org path the player would never reach it.
    x, y = find_start(data)
    start_position = x, y, Direction.up
    first_player_trace = run_from_here(data, start_position)
    print(len(first_player_trace))
    loopy_paths = []
    for i, position in enumerate(first_player_trace):
        print(i)
        if (position[0], position[1]) in loopy_paths:
            continue
        new_maze = maybe_add_obstacle(data, position)
        if not new_maze:
            continue
        player_trace = run_from_here(new_maze, start_position)
        if player_trace is None:
            loopy_paths.append((position[0], position[1]))
    return len(loopy_paths)


def maybe_add_obstacle(data, position):
    x, y, _ = position
    if data[y][x] != ".":
        return None
    new_data = data.copy()
    new_data[y] = data[y][:x] + "#" + data[y][x+1:]
    return new_data


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)

# add a loop detector
# loop over permutations of the map