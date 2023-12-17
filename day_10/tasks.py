import time
import numpy as np
import copy

default_distance = -1

directions = {
    "north": (-1, 0),
    "east": (0, 1),
    "west": (0, -1),
    "south": (1, 0)
}

PIPES = {
    "|": [directions["north"], directions["south"]],
    "-": [directions["east"], directions["west"]],
    "L": [directions["north"], directions["east"]],
    "J": [directions["north"], directions["west"]],
    "7": [directions["south"], directions["west"]],
    "F": [directions["south"], directions["east"]],
    ".": [None],
    "S": [None]
}


class Node:

    def __init__(self, position, direction, distance, lines):
        self.position = position
        self.direction = direction
        self.distance = distance
        self.symbol = lines[position[0]][position[1]]


def find_starting_point(lines) -> tuple:
    line_index = -1
    start_symbol = "S"
    for index in range(len(lines)):
        if start_symbol in lines[index]:
            line_index = index
            break
    position_index = lines[line_index].index(start_symbol)
    return tuple((line_index, position_index))


def get_first_pipes(lines, starting_point):
    pipes = []
    start_symbols = PIPES.keys()
    for direction in directions.values():
        position = np.add(starting_point, direction)
        # ensure the computed position is a valid index
        if np.min(position) == -1 or position[0] == len(lines) or position[1] == len(lines[0]):
            continue
        symbol = lines[position[0]][position[1]]
        for pipe_directions in PIPES[symbol]:
            if np.array_equal(np.multiply(direction, -1), pipe_directions):
                pipes.append(Node(position, direction, 1, lines))
                start_symbols = list(filter(lambda key: direction in PIPES[key], start_symbols))
                break
    return pipes, start_symbols[0]

def get_next_node(lines, current_node):
    pipe_directions = PIPES[current_node.symbol]
    for pipe_dir in pipe_directions:
        if not np.array_equal(pipe_dir, np.multiply(-1, current_node.direction)):
            return Node(np.add(current_node.position, pipe_dir), pipe_dir, current_node.distance + 1, lines)


def calculate_inner_area(distances, lines):
    area = 0
    inner_area_mask = copy.deepcopy(lines)
    for line_index in range(len(distances)):
        inside_loop = False
        loop_came_from_top = False
        for element_index in range(len(distances[0])):
            if distances[line_index][element_index] == default_distance:
                # position was not part of the loop, depending on inside_loop boolean increment area counter
                if inside_loop:
                    area += 1
                    inner_area_mask[line_index] = inner_area_mask[line_index][:element_index] + "I" \
                        + inner_area_mask[line_index][element_index + 1:]
            else:
                symbol = lines[line_index][element_index]
                if symbol == "|":
                    inside_loop = not inside_loop
                elif symbol == "-":
                    continue
                elif symbol == "L":
                    loop_came_from_top = True
                    inside_loop = not inside_loop
                elif symbol == "F":
                    loop_came_from_top = False
                    inside_loop = not inside_loop
                elif symbol == "J" and loop_came_from_top:
                    inside_loop = not inside_loop
                elif symbol == "7" and not loop_came_from_top:
                    inside_loop = not inside_loop
    return area


start_time = time.time()

# f = open("example5.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

start_pos = find_starting_point(lines)

distances = [[default_distance] * len(lines[0]) for _ in range(len(lines))]
distances[start_pos[0]][start_pos[1]] = 0

current_nodes, start_symbol = get_first_pipes(lines, start_pos)
lines[start_pos[0]] = lines[start_pos[0]][:start_pos[1]] + start_symbol + lines[start_pos[0]][start_pos[1] + 1:]

while current_nodes:
    current = current_nodes.pop(0)
    if distances[current.position[0]][current.position[1]] != default_distance:
        break
    else:
        distances[current.position[0]][current.position[1]] = current.distance

    next_node = get_next_node(lines, current)
    current_nodes.append(next_node)

maximal_distance = np.max(distances)
print(f"Maximal distance in loop is: {maximal_distance}")
print(f"Inner area of circle: {calculate_inner_area(distances, lines)}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
