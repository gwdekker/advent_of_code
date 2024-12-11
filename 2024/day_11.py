from collections import Counter
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return [int(stone) for stone in raw.split()]


data = parse_raw(raw)


def change(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0 :
        mid = len(str(stone)) // 2
        return [int(str(stone)[:mid]), int(str(stone)[mid:])]
    else:
        return [stone * 2024]


def part_one(data=data):
    stones = data
    for blink in range(25):
        stones = [new_stone for stone in stones for new_stone in change(stone)]
    return len(stones)


def part_two(data=data):
    stones = Counter(data)
    for blink in range(75):
        iterator = stones.copy()
        for stone_id, stone_count in iterator.items():
            new_stones = change(stone_id)
            for new_stone in new_stones:
                stones[new_stone] += stone_count
            stones[stone_id] -= stone_count
    return sum(stones.values())

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
