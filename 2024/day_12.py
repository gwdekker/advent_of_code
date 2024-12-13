from pathlib import Path
import aoc_helper


year = int(Path(__file__).parent.name)
day = int(__file__.removesuffix(".py").split("_")[-1])

raw = aoc_helper.fetch(day, year)


def parse_raw(raw: str):
    return raw.split()


data = parse_raw(raw)


def part_one(data=data):
    plots = gather_plots(data)
    regions = group_plots_into_regions(plots, data)
    perimeters = [sum(plot[1][1] for plot in region) for region in regions]
    areas = [len(region) for region in regions]
    return sum(perimeter * area for perimeter, area in zip(perimeters, areas))


def gather_plots(data):
    all_plots = dict()
    for x in range(len(data[0])):
        for y in range(len(data)):
            veggie_name = data[x][y]
            perimeter = calculate_perimeter((x, y), veggie_name, data)
            all_plots[(x, y)] = (data[x][y], perimeter)
    return all_plots


def calculate_neighbor_coords(coords, data):
    x0, y0 = coords
    neighbor_coords = [
        (x0-1, y0),
        (x0+1, y0),
        (x0, y0-1),
        (x0, y0+1)
    ]
    return [
        coord for coord in neighbor_coords
        if (0 <= coord[0] < len(data[0]))
        if (0 <= coord[1] < len(data))
    ]


def calculate_perimeter(plot_coords, veggie_name, data):
    perimeter = 4
    for n in calculate_neighbor_coords(plot_coords, data):
        if data[n[0]][n[1]] == veggie_name:
            perimeter -= 1
    return perimeter

def group_plots_into_regions(plots, data):
    regions = []
    while plots:
        plot = plots.popitem()
        regions.append(grow_group(plot, plots, data))
    return regions


def grow_group(plot, plots, data):
    group = set()
    new_group_members = [plot]
    while new_group_members:
        iterator = new_group_members.copy()
        group.update(new_group_members)
        new_group_members = []
        for new_member in iterator:
            for n in calculate_neighbor_coords(new_member[0], data):
                if plots.get(n, (None,))[0] == new_member[1][0]:
                    new_group_members.append((n, plots[n]))
                    plots.pop(n)
    return group

def calculate_fences(regions, data):
    sides = []
    for region in regions:
        fences = []
        coords = [(x, y) for (x, y), _ in region]
        for plot in coords:
            x, y = plot
            # can i make a north fence:
            # - no plot on top
            if (x-1, y) not in coords:
                fences.append(('N', (x, y)))
            if (x+1, y) not in coords:
                fences.append(('S', (x, y)))
            if (x, y+1) not in coords:
                fences.append(('E', (x, y)))
            if (x, y-1) not in coords:
                fences.append(('W', (x, y)))

        first = fences.pop()
        grouped_fences = [{first}]
        while fences:
            fence = fences.pop()
            groups_belonging_to = set()
            for i, group in enumerate(grouped_fences):
                if belongs_to_group(fence, group):
                    group.add(fence)
                    groups_belonging_to.add(i)
            if len(groups_belonging_to) == 0:
                grouped_fences.append({fence})
            if len(groups_belonging_to) == 2:
                one, other = groups_belonging_to
                grouped_fences[one].update(grouped_fences[other])
                del grouped_fences[other]
            if len(groups_belonging_to) > 2:
                raise NotImplementedError

        sides.append(len(grouped_fences))
    return sides

def belongs_to_group(fence, group):
    group_type = next(iter(group))[0]
    fence_type = fence[0]
    if fence_type != group_type:
        return False
    x, y = fence[1]
    group_coords = [(x, y) for _, (x, y) in group]
    if fence_type in {"N", "S"}:
        if (x, y-1) in group_coords:
            return True
        if (x, y+1) in group_coords:
            return True
    if fence_type in {"E", "W"}:
        if (x-1, y) in group_coords:
            return True
        if (x+1, y) in group_coords:
            return True
    return False


def part_two(data=data):
    plots = gather_plots(data)
    regions = group_plots_into_regions(plots, data)
    fences = calculate_fences(regions, data)
    areas = [len(region) for region in regions]
    return sum(fence * area for fence, area in zip(fences, areas))
    pass

# aoc_helper.lazy_test(day=day, year=year, parse=parse_raw, solution=part_two)

# aoc_helper.lazy_submit(day=day, year=year, solution=part_one, data=data)
aoc_helper.lazy_submit(day=day, year=year, solution=part_two, data=data)
