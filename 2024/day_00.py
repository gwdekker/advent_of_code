import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return raw


data = parse_raw(raw)


def part_one(data=data):
    pass


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
