import time


class Mapping:
    def __init__(self, dst_start, src_start, num_elements):
        self.dst_start = dst_start
        self.src_start = src_start
        self.num_elements = num_elements

    def get_mapping(self, element_tuple) -> tuple:
        seed_start, num_seeds = element_tuple
        start_index = max(self.src_start, seed_start)
        if start_index >= self.src_start + self.num_elements \
                or start_index >= seed_start + num_seeds:
            return False, None, None, None

        start_delta = start_index - self.src_start
        dst_seed_start = self.dst_start + start_delta
        max_value = min(self.src_start + self.num_elements, seed_start + num_seeds)
        num_mapped_elements = max_value - start_index
        return True, start_index, dst_seed_start, num_mapped_elements


start_time = time.time()

# f = open("example.txt", "r")
f = open("data2.txt", "r")
lines = f.readlines()
lines = list(map(lambda line: line.replace("\n", ""), lines))
lines.append("")

seeds = list(map(int, lines[0][7:].split(" ")))
seeds = [tuple((seeds[i], seeds[i + 1])) for i in range(0, len(seeds), 2)]
print(seeds)
mappings = []
mapped_elements = []

for line in lines[3:]:
    if line == "":
        for seed_index in range(len(seeds)):
            for map in mappings:
                in_map, start_index_src, mapped_start, num_elements_mapped = map.get_mapping(seeds[seed_index])
                if in_map:
                    num_elements_before_mapped = start_index_src - seeds[seed_index][0]
                    num_elements_after_mapped = seeds[seed_index][1] - num_elements_before_mapped - num_elements_mapped
                    seeds[seed_index] = (seeds[seed_index][0], num_elements_before_mapped)
                    mapped_elements.append((mapped_start, num_elements_mapped))
                    seeds.append(tuple((start_index_src + num_elements_mapped, num_elements_after_mapped)))

        # print(f"Results after Mapping round: {seeds}")
        mappings = []
        seeds = list(filter(lambda element: element[1] > 0, seeds))
        seeds += mapped_elements
        mapped_elements = []
        continue
    elif not line[0].isdigit():
        continue

    parts = line.split(" ")
    mapping = Mapping(int(parts[0]), int(parts[1]), int(parts[2]))
    mappings.append(mapping)

end_time = time.time()

print(f"Final values: {seeds}")
print(f"Minimal value with min: {min(seeds)[0]}")
print(f"Time for program: {end_time - start_time}")
print(f"Number of value seeds: {len(seeds)}")
