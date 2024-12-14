from pathlib import Path
import aoc_helper
import re
import numpy as np


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    blocks = raw.split("\n\n")
    parsed = []
    pattern = r'(?P<button>A|B|Prize):\s*X[+=](?P<x>\d+),\s*Y[+=](?P<y>\d+)'
    for block in blocks:
        block_dict = dict()
        matches = re.finditer(pattern, block)
        for match in matches:
            d = match.groupdict()
            if d["button"] == "Prize":
                block_dict["x"] = int(d["x"])
                block_dict["y"] = int(d["y"])
            elif d["button"] == "A":
                block_dict["A_x"] = int(d["x"])
                block_dict["A_y"] = int(d["y"])
            elif d["button"] == "B":
                block_dict["B_x"] = int(d["x"])
                block_dict["B_y"] = int(d["y"])
            else:
                raise ValueError
        parsed.append(block_dict)
    return parsed


data = parse_raw(raw)


def part_one(data=data):
    costs = []
    for problem in data:
        a, b = solve_problem(problem)
        if a:
            costs.append(3*a + 1*b)
    return sum(costs)

def solve_problem(problem):
    for A in range(1, 100):
        B = int( (problem["x"] - problem["A_x"]*A) / problem["B_x"] )
        if A * problem["A_y"] + B * problem["B_y"] == problem["y"]:
            return A, B
    return None, None

def solve_problem2(problem):
    large = 10_000_000_000_000
    problem["x"] += large
    problem["y"] += large

    Mx = np.array([[problem["A_x"], problem["B_x"]], [problem["A_y"], problem["B_y"]]])
    b = np.array([problem["x"], problem["y"]])
    AB = np.linalg.solve(Mx, b)
    A, B = AB
    A = int(round(A, 0))
    B = int(round(B, 0))
    if A * problem["A_y"] + B * problem["B_y"] == problem["y"]:
        if A * problem["A_x"] + B * problem["B_x"] == problem["x"]:
            return A, B
        else:
            return None, None
    else:
        return None, None

def part_two(data=data):
    costs = []
    for problem in data:
        a, b = solve_problem2(problem)
        if a:
            costs.append(3*a + 1*b)
    return sum(costs)

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
