from collections import deque
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    return [tuple(map(int, line.split(","))) for line in raw.splitlines()]


data = parse_raw(raw)
max_x, max_y = 71, 71


def part_one(data=data):
    n_bytes_to_fall = 1024
    selected_data = data[:n_bytes_to_fall]
    print_grid(selected_data)
    start_coord = (0, 0)
    end_coord = (max_x-1, max_y-1)
    queue = deque()
    queue.append(start_coord)
    positions_reached = {start_coord: 0}
    while queue:
        coord0 = queue.popleft()
        new_positions = [
            coord for coord in valid_moves_in_grid(coord0)
            if coord not in selected_data
        ]
        new_cost = positions_reached[coord0] + 1
        for pos in new_positions:
            if pos not in positions_reached:
                positions_reached[pos] = new_cost
                queue.append(pos)
            elif positions_reached[pos] > new_cost:
                positions_reached[pos] = new_positions
                queue.append(pos)
            else:
                continue
    return positions_reached[end_coord]


def valid_moves_in_grid(coord):
    x, y = coord
    moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [
        move for move in moves
        if 0 <= move[0] < max_x
        if 0 <= move[1] < max_y
    ]



def print_grid(coords):
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print("\n", end='')
    print("")

part_one(data)


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
