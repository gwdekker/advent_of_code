import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    return raw.split()

data = parse_raw(raw)

def revert(data):
    return [d[::-1] for d in data]

def data_variants(data):
    transposed = ["".join(row) for row in zip(*data)]
    diagonals = get_diagonals(data)
    return [data, revert(data), transposed, revert(transposed), diagonals, revert(diagonals)]

def get_diagonals(data):
    n, m = len(data), len(data[0])
    diagonals = []

    # Get diagonals from top-left to bottom-right
    for d in range(n + m - 1):
        diagonals.append("".join(data[i][d - i] for i in range(max(0, d - m + 1), min(n, d + 1))))

    # Get diagonals from top-right to bottom-left
    for d in range(n + m - 1):
        diagonals.append("".join(data[i][i - d + m - 1] for i in range(max(0, d - m + 1), min(n, d + 1))))

    return diagonals


def part_one(data=data):
    to_find = "XMAS"
    counts = 0
    for data_variant in data_variants(data):
        counts += sum([line.count(to_find) for line in data_variant])
    return counts

def part_two(data=data):
    candidates = dict()
    for y in range(len(data)):
        for x in range(len(data[0])):
            try:
                candidate = "".join((data[y][x], data[y][x+2], data[y+1][x+1], data[y+2][x], data[y+2][x+2]))
            except IndexError:
                continue
            if is_valid(candidate):
                candidates[(y, x)] = candidate
    return len(candidates)

def is_valid(candidate):
    if candidate[2] != "A":
        return False
    if candidate.count("M") != 2:
        return False
    if candidate.count("S") != 2:
        return False
    if candidate in {"MSASM", "SMAMS"}:
        return False
    return True


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
