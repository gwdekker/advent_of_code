import time
from collections import Counter
from itertools import count
from pathlib import Path
import aoc_helper

import re
from pydantic import BaseModel

year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


class Robot(BaseModel):
    x: int
    y: int
    dx: int
    dy: int

class Grid(BaseModel):
    x: int
    y: int

    @property
    def initial_grid(self):
        return [[0 for _ in range(self.y)] for _ in range(self.x)]

    @property
    def mid_x(self):
        return self.x // 2

    @property
    def mid_y(self):
        return self.y // 2

    def print(self, grid):
        for y in range(self.y):
            for x in range(self.x):
                if grid[x][y] == 0:
                    print(' ', end='')
                else:
                    print(grid[x][y], end='')
            print("\n", end='')
        print("")



def parse_raw(raw: str):
    return [parse_line(line) for line in raw.splitlines()]

def parse_line(line: str):
    nr = r"-?\d+"
    x = rf"(?P<x>{nr})"
    y = rf"(?P<y>{nr})"
    dx = rf"(?P<dx>{nr})"
    dy = rf"(?P<dy>{nr})"
    pattern = rf"p={x},{y}\s+v={dx},{dy}"
    return Robot(**re.search(pattern, line).groupdict())


data = parse_raw(raw)


def part_one(data=data):
    p = Grid(
        x=101,
        y=103,
    )
    iters = 100
    robot_data = list()
    for d in data:
        x = (d.x + iters * d.dx) % p.x
        y = (d.y + iters * d.dy) % p.y
        robot_data.append(Robot(x=x, y=y, dx=d.dx, dy=d.dy))
    draw_grid(grid=p, robot_data = robot_data)
    return calculate_code(p, robot_data)


def calculate_code(grid, robot_data):
    q1 = len([r for r in robot_data if r.x < grid.mid_x if r.y < grid.mid_y])
    q2 = len([r for r in robot_data if r.x > grid.mid_x if r.y < grid.mid_y])
    q3 = len([r for r in robot_data if r.x < grid.mid_x if r.y > grid.mid_y])
    q4 = len([r for r in robot_data if r.x > grid.mid_x if r.y > grid.mid_y])
    return q1*q2*q3*q4


def draw_grid(grid, robot_data):
    g = grid.initial_grid
    for robot in robot_data:
        g[robot.x][robot.y] += 1
    grid.print(g)


# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)

def part_two(data=data):
    p = Grid(
        x=101,
        y=103,
    )
    for i in count():
        if i % 1000 == 0:
            print(i)
        robot_data = list()
        for d in data:
            x = (d.x + i * d.dx) % p.x
            y = (d.y + i * d.dy) % p.y
            robot_data.append(Robot(x=x, y=y, dx=d.dx, dy=d.dy))
        if maybe_a_tree(robot_data):
            draw_grid(grid=p, robot_data = robot_data)
            print(i)

def maybe_a_tree(robot_data):
    # c = Counter([r.y for r in robot_data])
    # if max(c.values()) > 50:
    #     return True
    # return False
    coords = [(r.x, r.y) for r in robot_data]
    return len(coords) == len(set(coords))

part_two(data)


# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
# aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
