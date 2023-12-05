import time

seeds = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

# seeds = open("input.txt", "r").read()
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        seeds = open(sys.argv[1], "r").read()

seed_maps = [smap.split("\n") for smap in seeds.split("\n\n") if smap.strip()]

seed_numbers = [int(sn.strip()) for sn in seed_maps[0][0].split(" ")[1:] if sn.strip()]
maps_numbers = [
    [
        [int(sn.strip()) for sn in line.split(" ") if sn.strip()]
        for line in smap[1:]
        if line.strip()
    ]
    for smap in seed_maps[1:]
]


class MapRange:
    def __init__(self, start_src, start_dst, range_size):
        self.start_src = start_src
        self.start_dst = start_dst
        self.range_size = range_size

    def get(self, n):
        if self.start_src <= n < self.start_src + self.range_size:
            return self.start_dst + (n - self.start_src), True
        return n, False


## Generate all ranges
maps_ranges = []
for mn in maps_numbers:
    ## Number ranges
    map_range = []
    for r in mn:
        map_range.append(MapRange(r[1], r[0], r[2]))
    maps_ranges.append(map_range)


def process_seeds(seed):
    result = seed
    for map_range in maps_ranges:
        for mr in map_range:
            result, matched = mr.get(result)
            if matched:
                break
    return result


def main():
    min_seed_location = None

    global seed_numbers
    seed_numbers = [
        range(seed_numbers[i], seed_numbers[i] + seed_numbers[i+1])
        for i in range(0, len(seed_numbers), 2)
    ]
    print(seed_numbers)
    print("Ended expansion, calculate locations")
    for i, seeds in enumerate(seed_numbers):
        print("Calculate location for group", i + 1, "len", len(seeds))
        start = time.time()
        for loc in map(process_seeds, seeds):
            if min_seed_location is None or loc < min_seed_location:
                min_seed_location = loc
        print("Calculate location for group", i + 1, "len", len(seeds), f"(time {time.time()-start}s)")

    print(min_seed_location)


main()
