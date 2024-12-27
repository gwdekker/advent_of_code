from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return [int(x) for x in raw.splitlines()]


data = parse_raw(raw)


def part_one(data=data):
    new_secrets = [secret_2000(secret) for secret in data]
    return sum(new_secrets)


def mix(value, secret):
    return value ^ secret


def prune(secret):
    return secret % 16777216


assert mix(15, 42) == 37
assert prune(100000000) == 16113920


def next_secret(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret

list_of_secrets = [
    123,
    15887950,
    16495136,
    527345,
    704524,
    1553684,
    12683156,
    11100544,
    12249484,
    7753432,
    5908254,
]
for secret, secret2 in zip(list_of_secrets, list_of_secrets[1:]):
    assert next_secret(secret) == secret2

dummy_input = [1, 10, 100, 1024]


def secret_2000(seed):
    for i in range(2000):
        seed = next_secret(seed)
    return seed


assert secret_2000(1) == 8685429
assert secret_2000(10) == 4700978
assert secret_2000(100) == 15273692
assert secret_2000(2024) == 8667524


aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    pass

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
