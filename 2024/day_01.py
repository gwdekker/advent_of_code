from collections import Counter

import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    all_as_int = [int(x) for x in raw.split()]
    return all_as_int[::2], all_as_int[1::2]

data = parse_raw(raw)

def part_one(data=data):
    left, right = data
    return sum(abs(x-y) for x, y in zip(sorted(left), sorted(right)))

def part_two(data=data):
    left, right = data
    return sum(x * Counter(right)[x] for x in left)


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
