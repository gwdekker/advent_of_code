import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    data = []
    # add index to be able to track the original line nr later in the computation for deduplication
    for i, line in enumerate(raw.splitlines()):
        result, _, elms = line.partition(":")
        data.append((i, int(result), [int(elm) for elm in elms.split()]))
    return data

data = parse_raw(raw)

def main(data=data, round=1):
    candidates_this_round = data
    valid_lines = []
    candidates_next_round = []
    while candidates_this_round:
        for i, result, elms in candidates_this_round:
            if len(elms) == 1:
                raise NotImplementedError()
            if len(elms) == 2:
                if is_valid_two(result, elms, round):
                    valid_lines.append((i, result, elms))
            else:
                candidates_next_round.append((i, result, [elms[0] + elms[1], *elms[2:]]))
                candidates_next_round.append((i, result, [elms[0] * elms[1], *elms[2:]]))
                if round == 2:
                    candidates_next_round.append((i, result, [concat(elms[0], elms[1]), *elms[2:]]))
        candidates_this_round = candidates_next_round
        candidates_next_round = []
    valid_lines = set([(line_nr, result) for line_nr, result, _ in valid_lines])
    return sum(item[1] for item in valid_lines)


def is_valid_two(result, elms, round):
    if sum(elms) == result:
        return True
    if elms[0] * elms[1] == result:
        return True
    if round == 2 and concat(elms[0], elms[1]) == result:
        return True
    return False

def concat(elm1: int, elm2: int):
    return int(str(elm1) + str(elm2))

def part_one(data=data):
    return main(data, round=1)

def part_two(data=data):
    return main(data, round=2)

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
