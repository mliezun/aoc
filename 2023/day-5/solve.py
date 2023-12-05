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

seeds = open("input.txt", "r").read()

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
        print(r)
        map_range.append(MapRange(r[1], r[0], r[2]))
    maps_ranges.append(map_range)

# print(seed_numbers)
# print(maps_numbers)
# print(maps_ranges)

seeds_locations = []
for seed in seed_numbers:
    result = seed
    for map_range in maps_ranges:
        for mr in map_range:
            result, matched = mr.get(result)
            if matched:
                break
    seeds_locations.append(result)

print(seeds_locations)
print(min(seeds_locations))
