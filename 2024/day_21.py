import functools
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def numeric_keypad():
    return [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3],
        [None, 0, A]
    ]


def directional_keypad():
    return [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]

A = "A"
nk = numeric_keypad()
dk = directional_keypad()

@functools.lru_cache
def find(key, kind="numeric"):
    if kind == "numeric":
        key = A if key == A else int(key)
        return find_key(key, nk)
    else:
        return find_key(key, dk)


def find_key(key, keypad):
    for y, row in enumerate(keypad):
        if key in row:
            return y, row.index(key)


# @functools.lru_cache
def press_key(target_key, start_key, kind="numeric"):
    start_coord = find(start_key, kind=kind)
    target_coord = find(target_key, kind=kind)
    dx = target_coord[1] - start_coord[1]
    dy = target_coord[0] - start_coord[0]
    sequence = ""
    if dx > 0:
        sequence += ">" * dx
    if dx < 0:
        sequence += "<" * -dx
    if dy > 0:
        sequence += "v" * dy
    if dy < 0:
        sequence += "^" * -dy
    sequence += A

    def custom_sort_key(token):
        order = {">": 0, "^": 1, "v": 2, "<": 3, "A": 4}
        return order[token]
    if target_key == '7':
        pass
    tokens = list(sequence)
    new_sequence = ''.join(sorted(tokens, key=custom_sort_key))

    # todo: do some special casing to avoid the empty space.
    return new_sequence

def press_code(code, kind="numeric", start_key=A):
    sequence = ""
    for target_key in code:
        sequence += press_key(target_key, kind=kind, start_key=start_key)
        start_key = target_key
    return sequence

def parse_raw(raw: str):
    return raw


# data = parse_raw(raw)
data = """
029A
980A
179A
456A
379A
"""

def part_one(data=data):
    answers = {}
    for code in data.strip().splitlines():
        s = press_code(code, kind="numeric")
        s2 = press_code(s, kind="directional")
        s3 = press_code(s2, kind="directional")
        answers[code] = s3
    return sum([int(key[:-1])*len(val) for key, val in answers.items()])

part_one(data)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
