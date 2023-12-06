
class Mapping:
    def __init__(self, dst_start, src_start, num_elements):
        self.dst_start = dst_start
        self.src_start = src_start
        self.num_elements = num_elements

    def get_mapping(self, src_index) -> tuple:
        delta = src_index - self.src_start
        if delta < 0 or delta >= self.num_elements:
            return False, 0
        else:
            return True, self.dst_start + delta


# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda line: line.replace("\n", ""), lines))
lines.append("")

seeds = list(map(int, lines[0][7:].split(" ")))
print(seeds)
mappings = []

for line in lines[3:]:
    if line == "":
        for seed_index in range(len(seeds)):
            for map in mappings:
                in_map, mapped_value = map.get_mapping(seeds[seed_index])
                if in_map:
                    seeds[seed_index] = mapped_value
                    break
        # print(f"Results after Mapping round: {seeds}")
        mappings = []
        continue
    elif not line[0].isdigit():
        continue

    parts = line.split(" ")
    mapping = Mapping(int(parts[0]), int(parts[1]), int(parts[2]))
    mappings.append(mapping)

print(f"Final values: {seeds}")
print(f"minimal distance found: {min(seeds)}")
