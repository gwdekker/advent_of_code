import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return raw


data = parse_raw(raw)


def part_one(data=data):
    import re
    p_int = r"-?\d+"
    pattern = rf"mul\(({p_int}),({p_int})\)"
    matches = re.findall(pattern, data)
    multiplied = [int(x)*int(y) for x, y in matches]
    return sum(multiplied)


# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    import re
    p_int = r"-?\d+"
    pattern_mul = fr"(?P<mul>mul\(({p_int}),({p_int})\))"
    pattern_do = r"(?P<do>do\(\))"
    pattern_dont = r"(?P<dont>don't\(\))"
    combined_pattern = fr"{pattern_mul}|{pattern_do}|{pattern_dont}"
    matches = re.finditer(combined_pattern, data)
    do_mul = True
    result = 0
    for a_match in matches:
        if a_match.group("mul"):
            if not do_mul:
                continue
            x, y = map(int, a_match.groups()[1:3])
            result += x*y
        elif a_match.group("do"):
            do_mul = True
        elif a_match.group("dont"):
            do_mul = False
    return result

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
