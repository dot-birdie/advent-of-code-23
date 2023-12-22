import copy

import numpy as np
import math
from util_functions import timer_func, read_input
from queue import PriorityQueue


def get_field_value(lines, position):
    return int(lines[position[0]][position[1]])


def is_pos_on_field(position, num_rows, num_columns):
    return 0 <= position[0] < num_rows and 0 <= position[1] < num_columns


def get_new_pos(current_pos, direction):
    return tuple(np.add(current_pos, direction[:2]))


def get_rotation_matrix(angle, vector):
    theta = (angle / 180.) * np.pi
    vector = np.array(vector)
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                           [np.sin(theta), np.cos(theta)]])
    return np.dot(rot_matrix, vector).astype(int)


def try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, direction, current_loss):
    num_rows = len(lines)
    num_columns = len(lines[0])

    new_position = get_new_pos(position, direction)
    if is_pos_on_field(new_position, num_rows, num_columns):
        new_heat_loss = current_loss + get_field_value(lines, new_position)
        # Problem: can only move in 3 directions, therefore equal distance elements exist but are not equivalent!
        # increment with + 1 to ensure all with same distance but different direction are considered
        if new_heat_loss < minimal_field_distance[direction[2]][new_position[0]][new_position[1]][direction[:2]]:
            for i in range(2, direction[2] - 1, -1):
                minimal_field_distance[i][new_position[0]][new_position[1]][direction[:2]] = min(new_heat_loss,
                    minimal_field_distance[i][new_position[0]][new_position[1]][direction[:2]])
            nodes.put((new_heat_loss, new_position, direction))


def add_new_nodes(lines, nodes, minimal_field_distance, position, direction, current_heat_loss):
    if direction[2] < 2:
        straight_direction = (direction[0], direction[1], direction[2] + 1)
        try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, straight_direction, current_heat_loss)

    zero_padding_tuple = (0,)
    turn_left_direction = tuple(get_rotation_matrix(90, direction[:2])) + zero_padding_tuple
    try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, turn_left_direction, current_heat_loss)
    turn_right_direction = tuple(get_rotation_matrix(270, direction[:2])) + zero_padding_tuple
    try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, turn_right_direction, current_heat_loss)


def explore_field(lines, start_position, start_direction, goal_pos):
    nodes = PriorityQueue()
    nodes.put((0, start_position, start_direction))
    map_for_field = {
        (1, 0): math.inf,
        (-1, 0): math.inf,
        (0, -1): math.inf,
        (0, 1): math.inf
    }
    minimal_field_distance = [[[copy.deepcopy(map_for_field) for x in range(len(lines[0]))] for i in range(len(lines))] for j in range(3)]
    while nodes:
        current_node = nodes.get()
        heat_loss, current_pos, current_dir = current_node
        if current_pos == goal_pos:
            return heat_loss
        else:
            add_new_nodes(lines, nodes, minimal_field_distance, current_pos, current_dir, heat_loss)
    return -1


@timer_func
def main(filename):
    lines = read_input(filename)

    minimal_heat_loss = explore_field(lines, (0, 0), (0, 1, 0), (len(lines) - 1, len(lines[0]) - 1))
    #minimal_heat_loss = explore_field(lines, (0, 0), (0, 1, 0), (0, len(lines[0]) - 1))

    print(f"Minimal found heat loss is: {minimal_heat_loss}")


# main("example.txt")
main("data.txt")
