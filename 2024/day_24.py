from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)
# raw = """
# x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0
#
# x00 AND y00 -> z00
# x01 XOR y01 -> z01
# x02 OR y02 -> z02
# """

# raw = """
# x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1
#
# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj
# """


def parse_raw(raw: str):
    start_values, _, operations = raw.strip().partition("\n\n")
    start_values = {x.split(":")[0]: int(x.split(":")[1]) for x in start_values.split("\n")}
    ops = [[x for x in line.split(" ")] for line in operations.split("\n")]
    oplist = []
    for elm in ops:
        oplist.append(((elm[0], elm[1], elm[2]), elm[4]))
    return start_values, oplist

data = parse_raw(raw)

def operate(a: int, op: str, b: int) -> int | None:
    if a not in (0, 1) or b not in (0, 1):
        return None
    if op == "AND":
        return a & b
    elif op == "OR":
        return a | b
    elif op == "XOR":
        return a ^ b
    else:
        raise ValueError

def calculate_value(all_values):
    zs = {k:v for k,v in sorted(all_values.items()) if k.startswith("z")}
    out = 0
    for i, v in enumerate(zs.values()):
        out += v * (2 ** i)
    return out


def part_one(data=data):
    start_values, operations = data
    all_values = start_values.copy()
    for opstring, store in operations:
        a, op, b = opstring
        if a not in all_values:
            all_values[a] = None
        if b not in all_values:
            all_values[b] = None
        if store not in all_values:
            all_values[store] = None

    while any(value is None for value in all_values.values()):
        for opstring, store in operations:
            a, op, b = opstring
            a = all_values.get(a, None)
            b = all_values.get(b, None)
            result = operate(a, op, b)
            if result is not None:
                all_values[store] = result
    return calculate_value(all_values)



def part_two(data=data):
    pass

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
