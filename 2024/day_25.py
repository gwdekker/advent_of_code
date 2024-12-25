from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)
# raw = """
# #####
# .####
# .####
# .####
# .#.#.
# .#...
# .....
#
# #####
# ##.##
# .#.##
# ...##
# ...#.
# ...#.
# .....
#
# .....
# #....
# #....
# #...#
# #.#.#
# #.###
# #####
#
# .....
# .....
# #.#..
# ###..
# ###.#
# ###.#
# #####
#
# .....
# .....
# .....
# #....
# #.#..
# #.#.#
# #####
# """

def parse_raw(raw: str):
    key_or_locks = raw.strip().split("\n\n")
    kl_counts = []
    for elm in key_or_locks:
        what = "lock" if elm.startswith("#") else "key"
        counts = []
        s = elm.strip().split("\n")
        for i in range(len(s[0])):
            n = sum([x == "#" for x in [s[j][i] for j in range(len(s))]])
            counts.append(n-1)
        kl_counts.append((what, counts))
    return(kl_counts)


data = parse_raw(raw)


def part_one(data=data):
    keys = [x for x in data if x[0] == "key"]
    locks = [x for x in data if x[0] == "lock"]
    nr_matching_combos = 0
    for key in keys:
        for lock in locks:
            if is_a_match(key[1], lock[1]):
                nr_matching_combos += 1

    return nr_matching_combos

def is_a_match(key, lock):
    if any([x + y > 5 for x, y in zip(key, lock)]):
        return False
    return True

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
