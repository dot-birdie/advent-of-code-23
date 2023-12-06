# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
# @#!$%^&*()_+|~-=`{}[]:";'<>?,/
symbols = "@#!$%^&*()_+|~-=`{}[]:\";'<>?,/"


def get_neighborhood(lines, line_index, index, length):
    neighbor_lines = lines[max(0, line_index - 1):min(len(lines), line_index + 2)]
    neighbors = []
    for neighbor_line in neighbor_lines:
        neighbors += neighbor_line[max(0, index - 1):min(len(lines[line_index]), index + length + 1)]
    return neighbors


def is_a_symbol_adjacent(lines, line_index, index, length):
    neighborhood = get_neighborhood(lines, line_index, index, length)
    return any(character in symbols for character in neighborhood)


total = 0
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

        if is_a_symbol_adjacent(lines, line_index, index, length):
            number = int(line[index:index + length])
            total += number
        # else:
            # number = int(line[index:index + length])
            # print(f"Not identified as part number: {number}, line_index: {line_index}")

        index += length + 1

print(total)


