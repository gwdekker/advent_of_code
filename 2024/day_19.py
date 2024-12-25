from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    towels, _, patterns = raw.partition("\n\n")
    towels = towels.strip().split(", ")
    patterns = patterns.strip().split("\n")
    return towels, patterns

data = parse_raw(raw)


def part_one(data=data):
    towels, patterns = data
    solvable = set(towels)
    solvable.add("")
    unsolvable = set()
    for i, pattern in enumerate(patterns):
        print(i, len(solvable), pattern)
        if not can_be_made(pattern, towels, solvable, unsolvable):
            unsolvable.add(pattern)
    return len(patterns) - len(unsolvable)


def can_be_made(pattern, towels, solvable, unsolvable):
    if pattern in solvable:
        return True
    if pattern in unsolvable:
        return False
    for i in range(-1, -len(pattern)-1, -1):
        subpattern = pattern[i:]
        for towel in towels:
            if subpattern.startswith(towel) and subpattern.removeprefix(towel) in solvable and subpattern not in solvable:
                solvable.add(subpattern)
    return pattern in solvable

def part_two(data):
    towels, patterns = data
    solvable = set(towels)
    unsolvable = set()
    for i, pattern in enumerate(patterns):
        print("part1", i, len(solvable), pattern)
        if not can_be_made(pattern, towels, solvable, unsolvable):
            unsolvable.add(pattern)
    solvable_patterns = [pattern for pattern in patterns if pattern in solvable]
    n_ways = 0
    for p in solvable_patterns:
        print(p)
        ways = {(t, (t,)) for t in towels}
        for i in range(-1, -len(p)-1, -1):
            subpattern = p[i:]
            for towel in towels:
                if subpattern.startswith(towel):
                    if subpattern.removeprefix(towel) in [x[0] for x in ways]:
                        for way in ways.copy():
                            if way[0] == subpattern.removeprefix(towel):
                                new_way = (subpattern, (subpattern, *way[1]))
                                ways.add(new_way)
        n_ways += len([way for way in ways if way[0] == p])
    return n_ways


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
