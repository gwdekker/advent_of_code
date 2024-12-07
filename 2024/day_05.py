import aoc_helper

year = 2024
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    def parse(tup):
        x, _, y = tup.partition("|")
        return int(x), int(y)
    tups, _, lists = raw.partition("\n\n")
    ordering_rules = [parse(t) for t in tups.split()]
    updates = [[int(elm) for elm in manual.split(',')] for manual in lists.split()]
    return ordering_rules, updates

data = parse_raw(raw)

def part_one(data=data):
    ordering_rules, updates = data

    valid_updates = []
    for update in updates:
        applicable_rules_for_update = find_rules_for_update(ordering_rules, update)
        if update_is_valid(update, rules=applicable_rules_for_update):
            valid_updates.append(update)
    return sum_middle_numbers_of_lists(valid_updates)

def find_rules_for_update(ordering_rules, update):
    applicable_rules_for_update = set()
    for nr in update:
        applicable_rules_for_nr = [tup for tup in ordering_rules if tup[0] == nr if tup[1] in update]
        applicable_rules_for_update.update(applicable_rules_for_nr)
    return applicable_rules_for_update

def update_is_valid(update, rules):
    for rule in rules:
        if update.index(rule[0]) > update.index(rule[1]):
            return False
    return True

def sum_middle_numbers_of_lists(lists: list[list[int]]):
    return sum(lst[(len(lst)//2)] for lst in lists)


def part_two(data=data):
    ordering_rules, updates = data

    reordered_updates = []
    for update in updates:
        applicable_rules_for_update = find_rules_for_update(ordering_rules, update)
        if update_is_valid(update, rules=applicable_rules_for_update):
            continue

        # This is the key: the len of the resulting dict indicates how much numbers the nr needs to be in front of.
        # So sorting by the number of numbers the number needs to be behind gives a valid order (apparently).
        # As this is mathematically not water tight, there is the extra check
        rules_dict = dict()
        for nr in update:
            rules_dict[nr] = [t[1] for t in applicable_rules_for_update if t[0] == nr]
        new_update = sorted(rules_dict, key=lambda d: len(rules_dict[d]), reverse=True)
        reordered_updates.append(new_update)
        if not update_is_valid(new_update, applicable_rules_for_update):
            raise ValueError
    return sum_middle_numbers_of_lists(reordered_updates)

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
