
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
    
    def intersect(self, other: range):
        """Intersection between ranges.
        Possible ways of intersecting [a b] and [c d]:
            [a   [c   d]   b]
            [a   [c  b]    d]
            [c   [a  b]    d]
            [c   [a  d]    b]

        Args:
            other (MapRange): Intersect with this range.

        Returns:
            tuple[range, bool]: Intersection and flag indicating if matched.
        """
        # [a   [c   d]   b]
        # [a   [c  b]    d]
        if self.start_src <= other.start < self.start_src + self.range_size:
            # [a   [c   d]   b]
            if other.start < self.start_src + self.range_size:
                return [
                    # range(self.start_src, other.start),
                    range(self.start_dst + (other.start - self.start_src), self.start_dst + (other.stop - self.start_src)),
                    # range(other.stop, self.start_src + self.range_size),
                ], True
            # [a   [c  b]    d]
            else:
                return [
                    # range(self.start_src, other.start),
                    range(self.start_dst + (other.start - self.start_src), self.start_dst + self.range_size),
                    range(self.start_src + self.range_size, other.stop),
                ], True
        # [c   [a  b]    d]
        # [c   [a  d]    b]
        if other.start <= self.start_src < other.stop:
            # [c   [a  b]    d]
            if self.start_src + self.range_size < other.stop:
                return [
                    range(other.start, self.start_src),
                    range(self.start_dst, self.start_dst + self.range_size),
                    range(self.start_src + self.range_size, other.stop),
                ], True
            # [c   [a  d]    b]
            else:
                return [
                    range(other.start, self.start_src),
                    range(self.start_dst, self.start_dst + (other.stop - self.start_src)),
                    # range(other.stop, self.start_src + self.range_size),
                ], True
        return [other], False

## Generate all ranges
maps_ranges = []
for mn in maps_numbers:
    ## Number ranges
    map_range = []
    for r in mn:
        map_range.append(MapRange(r[1], r[0], r[2]))
    maps_ranges.append(map_range)


def main():
    seed_ranges = [
        range(seed_numbers[i], seed_numbers[i] + seed_numbers[i + 1])
        for i in range(0, len(seed_numbers), 2)
    ]
    input_ranges = seed_ranges
    while maps_ranges:
        result_ranges = []
        mrs = maps_ranges.pop(0)
        for inr in input_ranges:
            for mr in mrs:
                result, matched = mr.intersect(inr)
                if matched:
                    break
            result_ranges.extend(result)
        input_ranges = result_ranges

    print("result:", min(input_ranges, key=lambda x: x.start).start)
        


if __name__ == "__main__":
    main()
