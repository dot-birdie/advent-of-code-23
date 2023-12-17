import time
import numpy as np

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
    for direction in directions.values():
        position = np.add(starting_point, direction)
        # ensure the computed position is a valid index
        if np.min(position) == -1 or position[0] == len(lines) or position[1] == len(lines[0]):
            continue
        symbol = lines[position[0]][position[1]]
        for pipe_directions in PIPES[symbol]:
            if np.array_equal(np.multiply(direction, -1), pipe_directions):
                pipes.append(Node(position, direction, 1, lines))
                break
    return pipes


def get_next_node(lines, current_node):
    pipe_directions = PIPES[current_node.symbol]
    for pipe_dir in pipe_directions:
        if not np.array_equal(pipe_dir, np.multiply(-1, current_node.direction)):
            return Node(np.add(current_node.position, pipe_dir), pipe_dir, current_node.distance + 1, lines)


start_time = time.time()

# f = open("example2.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

start_pos = find_starting_point(lines)

distances = [[-1] * len(lines[0]) for _ in range(len(lines))]
distances[start_pos[0]][start_pos[1]] = 0

current_nodes = get_first_pipes(lines, start_pos)

while current_nodes:
    current = current_nodes.pop(0)
    if distances[current.position[0]][current.position[1]] != -1:
        break
    else:
        distances[current.position[0]][current.position[1]] = current.distance

    next_node = get_next_node(lines, current)
    current_nodes.append(next_node)

# print(distances)
maximal_distance = np.max(distances)
print(f"Maximal distance in loop is: {maximal_distance}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
