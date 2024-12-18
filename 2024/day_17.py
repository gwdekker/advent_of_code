import dataclasses
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)
# raw = """
# Register A: 729
# Register B: 0
# Register C: 0
#
# Program: 0,1,5,4,3,0
# """

@dataclasses.dataclass
class Register:
    A: int
    B: int
    C: int

def parse_raw(raw: str):
    regs, program = raw.split("\n\n")
    for line in regs.split("\n"):
        if line.startswith("Register A: "):
            a = int(line.removeprefix("Register A: "))
        elif line.startswith("Register B: "):
            b = int(line.removeprefix("Register B: "))
        elif line.startswith("Register C: "):
            c = int(line.removeprefix("Register C: "))
    r = Register(A=a, B=b, C=c)
    program = [int(x) for x in program.removeprefix("Program: ").split(",")]
    return r, program


data = parse_raw(raw)


def part_one(data=data):
    r, program = data
    outputs = run_program(program, r)
    return ",".join(map(str, outputs))


def run_program(program, r):
    pointer = 0
    outputs = []
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]
        # print(f"{pointer=}, {opcode=}, {operand=}")
        new_pointer, output = run_instruction(opcode, operand, r)
        if output is not None:
            outputs.append(output)
        if new_pointer is not None:
            pointer = new_pointer
        else:
            pointer += 2
        print(f"{outputs=}")
    return outputs


def run_instruction(opcode: int, operand: int, r: Register) -> tuple[int|None, int|None]:
    match opcode:
        case 0: #adv
            r.A = r.A // (2 ** combo(operand, r))
        case 1: #bxl
            r.B = r.B ^ operand
        case 2: #bst
            r.B = combo(operand, r) % 8
        case 3: #jnz
            if r.A == 0:
                return None, None
            pointer = operand
            return pointer, None
        case 4: #bxc
            r.B = r.B ^ r.C
        case 5: #out
            output = combo(operand, r) % 8
            return None, output
        case 6: #bdv
            r.B = r.A // (2 ** combo(operand, r))
        case 7: #cdv
            r.C = r.A // (2 ** combo(operand, r))
        case _:
            raise ValueError
    return None, None

def combo(operand, register):
    if operand in {0, 1, 2, 3}:
        return operand
    elif operand == 4:
        return register.A
    elif operand == 5:
        return register.B
    elif operand == 6:
        return register.C
    else:
        raise ValueError



def part_two(data=data):
    pass



def test_0():
    r = Register(A=0, B=0, C=9)
    program = [2,6]
    run_program(program, r)
    assert r.B == 1

def test_1():
    r = Register(A=10, B=0, C=0)
    program = [5,0,5,1,5,4]
    outputs = run_program(program, r)
    assert outputs == [0, 1, 2]

def test_2():
    r = Register(A=2024, B=0, C=0)
    program = [0,1,5,4,3,0]
    outputs = run_program(program, r)
    assert outputs == [ 4,2,5,6,7,7,7,7,3,1,0]
    assert r.A == 0

def test_3():
    r = Register(A=0, B=29, C=0)
    program = [1,7]
    _ = run_program(program, r)
    assert r.B == 26

def test_4():
    r = Register(A=0, B=2024, C=43690)
    program = [4,0]
    _ = run_program(program, r)
    assert r.B == 44354

def test_5():
    r = Register(A=117440, B=0, C=0)
    program = [0,3,5,4,3,0]
    output = run_program(program, r)
    assert output == program

test_0()
test_1()
test_2()
test_3()
test_4()
test_5()

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)
# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
# aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
