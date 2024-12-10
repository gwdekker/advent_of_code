from collections import Counter
from itertools import groupby, count
from operator import mod
from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)

def parse_raw(raw: str):
    raw = [int(x) for x in raw]
    file_id = 0
    disk_map = dict()
    disk_head_pos = 0
    for i, len_elms in enumerate(raw):
        if is_file(i):
            for idx_on_disk in range(disk_head_pos, disk_head_pos+len_elms):
                disk_map[idx_on_disk] = file_id
            file_id += 1
        disk_head_pos += len_elms
    return disk_map

def is_file(i: int):
    return not (i % 2)


data = parse_raw(raw)

def part_one(data=data):
    defragmented = defragment(data)
    return checksum(defragmented)

def checksum(data):
    return sum([key*value for key, value in data.items()])

def defragment(data=data):
    empty_spots = [i for i in range(max(data.keys())) if i not in data.keys()]
    map_copy = data.copy()
    for empty_spot, (key, value) in zip(empty_spots, reversed(map_copy.items())):
        if key < empty_spot:
            break
        data[empty_spot] = value
        del data[key]
    return data

def defragment_blocks(data=data):
    data_blocks = dict()
    counted = Counter(data.values())
    for key, val in data.items():
        if (val, counted[val]) not in data_blocks.values():
            data_blocks[key] = (val, counted[val])
    empty_blocks = dict()
    consecutive = 0
    for i in range(max(data.keys())):
        if i in data.keys():
            if consecutive == 0:
                continue
            else:
                empty_blocks[i-consecutive] = (None, consecutive)
                consecutive = 0
        else:
            consecutive += 1

    has_changed = True
    i = 0
    while has_changed:
        has_changed = False
        iter_datablocks = data_blocks.copy()
        iter_emptyblocks = empty_blocks.copy()
        has_changed, data_blocks, empty_blocks = _inside_loop(data_blocks, empty_blocks, has_changed, iter_datablocks, iter_emptyblocks)

    new_data = dict()
    for key, (id_data, len_data) in sorted(data_blocks.items()):
        for i in range(len_data):
            new_data[key+i] = id_data
    return new_data


def _inside_loop(data_blocks, empty_blocks, has_changed, iter_datablocks, iter_emptyblocks):
    for loc_data, (id_data, len_data) in sorted(iter_datablocks.items(), reverse=True):
        for loc_empty, (_, len_empty) in sorted(iter_emptyblocks.items()):
            if (len_data <= len_empty) and (loc_empty < loc_data):
                data_blocks[loc_empty] = (id_data, len_data)
                del data_blocks[loc_data]
                del empty_blocks[loc_empty]
                if len_data < len_empty:
                    empty_blocks[loc_empty + len_data] = (None, len_empty - len_data)
                has_changed = True
                return has_changed, data_blocks, empty_blocks
    return has_changed, data_blocks, empty_blocks


empty_spots = [i for i in range(max(data.keys())) if i not in data.keys()]


# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_one)


def part_two(data=data):
    result = defragment_blocks(data)
    return checksum(result)

aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
