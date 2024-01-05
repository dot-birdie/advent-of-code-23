import copy

import numpy as np
import math
from util_functions import timer_func, read_input

blank_character = "."
dig_character = "#"

directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}


def fill_left(terrain, expansion_size):
    for line_index in range(len(terrain)):
        terrain[line_index] = blank_character * expansion_size + terrain[line_index]
    return terrain


def fill_right(terrain, expansion_size):
    for line_index in range(len(terrain)):
        terrain[line_index] = terrain[line_index] + blank_character * expansion_size
    return terrain


def fill_upwards(terrain, expansion_size):
    new_terrain = [blank_character * len(terrain[0]) for i in range(expansion_size)]
    terrain = new_terrain + terrain
    return terrain


def fill_downwards(terrain, expansion_size):
    new_terrain = [blank_character * len(terrain[0]) for i in range(expansion_size)]
    terrain = terrain + new_terrain
    return terrain


def get_new_position(current_position, direction):
    return tuple(np.add(current_position, direction))


def is_in_terrain_bounds(terrain, position):
    return 0 <= position[0] < len(terrain) and 0 <= position[1] < len(terrain[0])


def expand_terrain(terrain, current_position, new_position):
    if new_position[0] < 0:
        expansion_size = abs(new_position[0])
        return fill_upwards(terrain, expansion_size), (current_position[0] + expansion_size, current_position[1]), \
            (0, new_position[1])
    elif new_position[1] < 0:
        expansion_size = abs(new_position[1])
        return fill_left(terrain, expansion_size), (current_position[0], current_position[1] + expansion_size), \
            (new_position[0], 0)
    elif new_position[0] >= len(terrain):
        return fill_downwards(terrain, new_position[0] + 1 - len(terrain)), current_position, new_position
    elif new_position[1] >= len(terrain[0]):
        return fill_right(terrain, new_position[1] + 1 - len(terrain[0])), current_position, new_position


def dig_at_index(terrain, row_index, column_index):
    terrain[row_index] = terrain[row_index][:column_index] + dig_character + terrain[row_index][column_index + 1:]


def dig_line(terrain, current_position, new_direction):
    if new_direction[0] == 0:
        sign = np.sign(new_direction[1])
        for j in range(1, abs(new_direction[1]) + 1):
            dig_at_index(terrain, current_position[0], current_position[1] + sign * j)
    else:
        sign = np.sign(new_direction[0])
        for i in range(1, abs(new_direction[0]) + 1):
            dig_at_index(terrain, current_position[0] + sign * i, current_position[1])


def check_all_lines_equal_length(terrain):
    for line in terrain:
        if len(line) != len(terrain[0]):
            return False
    return True


def dig_lagoon(inputs):
    terrain = ["#"]
    current_position = (0, 0)

    for direction_char, quantity, color_code in inputs:
        new_direction = tuple(np.multiply(quantity, directions[direction_char]))
        new_position = get_new_position(current_position, new_direction)
        if not is_in_terrain_bounds(terrain, new_position):
            terrain, current_position, new_position = expand_terrain(terrain, current_position, new_position)

        dig_line(terrain, current_position, new_direction)
        current_position = new_position
    return terrain


def is_digged_left(terrain, row_index, column_index):
    return column_index - 1 >= 0 and terrain[row_index][column_index - 1] == dig_character


def is_digged_right(terrain, row_index, column_index):
    return column_index + 1 < len(terrain[0]) and terrain[row_index][column_index + 1] == dig_character


def is_digged_top(terrain, row_index, column_index):
    return row_index - 1 >= 0 and terrain[row_index - 1][column_index] == dig_character


def is_digged_bottom(terrain, row_index, column_index):
    return row_index + 1 < len(terrain) and terrain[row_index + 1][column_index] == dig_character


def is_horizontal_line(terrain, row_index, column_index):
    return is_digged_left(terrain, row_index, column_index) and is_digged_right(terrain, row_index, column_index)


def is_vertical_line(terrain, row_index, column_index):
    return is_digged_top(terrain, row_index, column_index) and is_digged_bottom(terrain, row_index, column_index)


def is_L_shape(terrain, row_index, column_index):
    return is_digged_top(terrain, row_index, column_index) and is_digged_right(terrain, row_index, column_index)


def is_F_shape(terrain, row_index, column_index):
    return is_digged_bottom(terrain, row_index, column_index) and is_digged_right(terrain, row_index, column_index)


def is_J_shape(terrain, row_index, column_index):
    return is_digged_top(terrain, row_index, column_index) and is_digged_left(terrain, row_index, column_index)


def is_7_shape(terrain, row_index, column_index):
    return is_digged_bottom(terrain, row_index, column_index) and is_digged_left(terrain, row_index, column_index)


def dig_out_inside(terrain):
    inside_dig_terrain = copy.deepcopy(terrain)
    for line_index in range(len(terrain)):
        inside_loop = False
        came_from_top = None
        for i in range(len(terrain[0]) - 1):
            if terrain[line_index][i] == blank_character:
                if inside_loop:
                    dig_at_index(inside_dig_terrain, line_index, i)
            else:
                if is_vertical_line(terrain, line_index, i):
                    inside_loop = not inside_loop
                elif is_horizontal_line(terrain, line_index, i):
                    continue
                elif is_L_shape(terrain, line_index, i):
                    came_from_top = True
                    inside_loop = not inside_loop
                elif is_F_shape(terrain, line_index, i):
                    came_from_top = False
                    inside_loop = not inside_loop
                elif is_J_shape(terrain, line_index, i) and came_from_top:
                    inside_loop = not inside_loop
                elif is_7_shape(terrain, line_index, i) and not came_from_top:
                    inside_loop = not inside_loop
    return inside_dig_terrain


def count_num_digs(terrain):
    total = 0
    for line in terrain:
        total += line.count(dig_character)
    return total


def get_inputs(lines):
    inputs = []
    for line in lines:
        direction, quantity, color_code = line.split(" ")
        inputs.append((direction, int(quantity), color_code[2:-1]))
    return inputs


def get_instructions_from_color_codes(inputs):
    modified_inputs = []
    color_directions = ["R", "D", "L", "U"]
    for i, j, color_code in inputs:
        dec = int(color_code[:5], 16)
        direction = color_directions[int(color_code[5])]
        modified_inputs.append((direction, dec))
    return modified_inputs


def task_1(inputs):
    terrain = dig_lagoon(inputs)
    inside_digged_terrain = dig_out_inside(terrain)
    all_same_length = check_all_lines_equal_length(inside_digged_terrain)
    print(f"Valid terrain: {all_same_length}")
    print(f"Total volume of lagoon: {count_num_digs(inside_digged_terrain)}")


def task_2(inputs):
    modified_inputs = get_instructions_from_color_codes(inputs)
    print(modified_inputs)


@timer_func
def main(filename):
    lines = read_input(filename)
    inputs = get_inputs(lines)
    task_1(inputs)
    task_2(inputs)


main("example.txt")
# main("data.txt")
