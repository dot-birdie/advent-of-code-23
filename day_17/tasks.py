import copy

import numpy as np
import math
from util_functions import timer_func, read_input
from queue import PriorityQueue

directions = {
    (-1, 0): 0,
    (1, 0): 1,
    (0, -1): 2,
    (0, 1): 3
}

def get_field_value(lines, position):
    return int(lines[position[0]][position[1]])

def is_legal_turn(position, direction, min_straight_steps, num_rows, num_columns):
    future_pos = position + ((min_straight_steps + 1) * direction[0], (min_straight_steps + 1) * direction[2])
    return is_pos_on_field(future_pos, num_rows, num_columns)

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


def override_minimal_distances(new_position, direction, new_heat_loss, minimal_field_distance, min_straight_steps, max_straight_steps):
    # Problem: can only move in 3 directions, therefore equal distance elements exist but are not equivalent!
    found_improvement = False
    for node_direction in directions.keys():
        if node_direction == (-1 * direction[0], -1 * direction[1]):
            continue
        if new_heat_loss < minimal_field_distance[direction[2]][new_position[0]][new_position[1]][directions[node_direction]]:
            found_improvement = True
            if direction[2] < min_straight_steps:
                minimal_field_distance[direction[2]][new_position[0]][new_position[1]][directions[node_direction]] = \
                    min(new_heat_loss,
                        minimal_field_distance[direction[2]][new_position[0]][new_position[1]][directions[node_direction]])
            else:
                for i in range(max_straight_steps - 1, direction[2] - 1, -1):
                    minimal_field_distance[i][new_position[0]][new_position[1]][directions[node_direction]] = \
                        min(new_heat_loss,
                            minimal_field_distance[i][new_position[0]][new_position[1]][directions[node_direction]])
    return found_improvement

def try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, direction, current_loss, min_straight_steps, max_straight_steps):
    num_rows = len(lines)
    num_columns = len(lines[0])
    # if the turn does not have sufficient num fields straight ahead it is illegal to follow this path
    if direction[2] and not is_legal_turn(position, direction, min_straight_steps, num_rows, num_columns):
        return

    new_position = get_new_pos(position, direction)
    found_improvement = False
    if is_pos_on_field(new_position, num_rows, num_columns):
        new_heat_loss = current_loss + get_field_value(lines, new_position)
        found_improvement = override_minimal_distances(new_position, direction, new_heat_loss, minimal_field_distance,
                                                       min_straight_steps, max_straight_steps)

    if found_improvement:
        nodes.put((new_heat_loss, new_position, direction))


def add_new_nodes(lines, nodes, minimal_field_distance, position, direction, current_heat_loss, min_straight_steps, max_straight_steps):
    if direction[2] < max_straight_steps - 1:
        straight_direction = (direction[0], direction[1], direction[2] + 1)
        try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, straight_direction, current_heat_loss, min_straight_steps, max_straight_steps)

    if direction[2] >= min_straight_steps:
        zero_padding_tuple = (0,)
        turn_left_direction = tuple(get_rotation_matrix(90, direction[:2])) + zero_padding_tuple
        try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, turn_left_direction, current_heat_loss, min_straight_steps, max_straight_steps)
        turn_right_direction = tuple(get_rotation_matrix(270, direction[:2])) + zero_padding_tuple
        try_append_to_pos_direction_list(lines, nodes, minimal_field_distance, position, turn_right_direction, current_heat_loss, min_straight_steps, max_straight_steps)


def explore_field(lines, start_position, start_direction, goal_pos, min_straight_steps, max_straight_steps):
    nodes = PriorityQueue()
    nodes.put((0, start_position, start_direction))
    map_for_field = [math.inf] * 4
    minimal_field_distance = [[[copy.deepcopy(map_for_field) for x in range(len(lines[0]))] for i in range(len(lines))] for j in range(max_straight_steps)]
    while nodes.queue:
        current_node = nodes.get()
        heat_loss, current_pos, current_dir = current_node
        if current_pos == goal_pos and current_dir[2] >= min_straight_steps:
            return heat_loss
        else:
            add_new_nodes(lines, nodes, minimal_field_distance, current_pos, current_dir, heat_loss, min_straight_steps, max_straight_steps)
    return -1


@timer_func
def main(filename):
    lines = read_input(filename)
    min_straight_steps = 0
    max_straight_steps = 3
    src_pos = (0, 0)
    dst_pos = (len(lines) - 1, len(lines[0]) - 1)
    # minimal_heat_loss_initial = explore_field(lines, src_pos, (0, 1, 0), dst_pos, 0, 3)
    # print(f"Minimal found initial heat loss is: {minimal_heat_loss_initial}")

    minimal_heat_loss_modified = explore_field(lines, src_pos, (0, 1, 0), dst_pos, 3, 9)
    print(f"Minimal found modified heat loss is: {minimal_heat_loss_modified}")


print("Goal: 94")
main("example.txt")
print("Goal: 71")
main("example2.txt")
# main("data.txt")
