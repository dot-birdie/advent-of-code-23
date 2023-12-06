


# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
gear = "*"


def get_gear_positions(lines, line_index, index, length):
    gear_positions = []
    line_length = len(lines[0])
    for index1 in range(max(0, line_index - 1), min(len(lines), line_index + 2)):

        for index2 in range(max(0, index - 1), min(line_length, index + length + 1)):
            if lines[index1][index2] == gear:
                gear_positions.append(index1 * line_length + index2)
    return gear_positions


gear_num_pairs = []
for line_index in range(len(lines)):
    line = lines[line_index]
    line_length = len(line)
    index = 0
    while index < line_length:
        if not line[index].isdigit():
            index += 1
            continue

        length = 1
        while index + length < line_length and line[index + length].isdigit():
            length += 1

        number = int(line[index:index + length])
        gear_positions = get_gear_positions(lines, line_index, index, length)
        for gear_pos in gear_positions:
            gear_num_pairs.append((gear_pos, number))

        index += length + 1

gear_num_pairs.sort()

total = 0
num_gear_num_pairs = len(gear_num_pairs)
for index in range(num_gear_num_pairs - 1):
    if gear_num_pairs[index][0] == gear_num_pairs[index + 1][0] \
            and (index + 2 >= num_gear_num_pairs or gear_num_pairs[index][0] != gear_num_pairs[index + 2][0]):
        total += gear_num_pairs[index][1] * gear_num_pairs[index + 1][1]

print(total)
