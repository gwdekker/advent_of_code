import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return [[int(c) for c in line.split()] for line in raw.splitlines()]


data = parse_raw(raw)

def sign(x: int):
    return (x > 0) - (x < 0)

def sign_diff(x: int, y: int):
    return sign(x - y)

def safe_diff(x: int, y: int):
    return abs(x-y) <= 3

def all_elms_same(lst: list[int]):
    return all(lst[0] == x for x in lst)

def left_one_out(lst):
    return [lst[:i] + lst[i+1:] for i in range(len(lst))]

def is_safe(lst):
    is_same = all_elms_same([sign_diff(a, b) for a, b in zip(lst, lst[1:])])
    is_small_diff = all([safe_diff(a, b) for a, b in zip(lst, lst[1:])])
    return is_same and is_small_diff


def part_one(data=data):
    i_safe = 0
    for line in data:
        if is_safe(line):
            i_safe += 1
    return i_safe

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    i_safe = 0
    for line in data:
        if is_safe(line):
            i_safe += 1
            continue
        for left_out in left_one_out(line):
            if is_safe(left_out):
                i_safe += 1
                break
    return i_safe

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
