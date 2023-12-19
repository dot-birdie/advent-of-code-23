import numpy as np
import math
import tqdm
import copy
from util_functions import timer_func, read_input


def rotate_anti_clockwise(lines):
    rotated_field = ["" for i in range(len(lines[0]))]
    for i in range(len(lines[0])):
        for j in range(len(lines)):
            rotated_field[i] = rotated_field[i] + lines[len(lines) - 1 - j][i]
    return rotated_field


def move_stone(lines, column, src_row, dst_row):
    lines[dst_row] = lines[dst_row][:column] + "O" + lines[dst_row][column + 1:]
    lines[src_row] = lines[src_row][:column] + "." + lines[src_row][column + 1:]


def tilt_north(lines):
    tilted_lines = copy.deepcopy(lines)
    for column in range(len(tilted_lines[0])):
        last_solid_index = -1
        for row in range(len(tilted_lines)):
            if tilted_lines[row][column] == "#":
                last_solid_index = row
            elif tilted_lines[row][column] == "O":
                last_solid_index += 1
                if row != last_solid_index:
                    move_stone(tilted_lines, column, row, last_solid_index)
    return tilted_lines


def count_weight(lines):
    weight = len(lines)
    total_weight = 0
    for line in lines:
        total_weight += weight * line.count("O")
        weight -= 1
    return total_weight


def do_cycle(board):
    for direction in range(4):
        board = tilt_north(board)
        board = rotate_anti_clockwise(board)
    return board


def rotate_and_tilt_cycle(initial_board, num_cycles):
    board = copy.deepcopy(initial_board)
    board_states = {}
    cycle = 0
    while cycle < num_cycles:
        if not tuple(board) in board_states:
            board_states[tuple(board)] = (cycle, -1)
            board = do_cycle(board)
            cycle += 1
        else:
            loop_opened, loop_closed = board_states[tuple(board)]
            if loop_closed == -2:
                board = do_cycle(board)
                cycle += 1
                continue

            if loop_closed == -1:
                board_states[tuple(board)] = (loop_opened, cycle)
                cycle_duration = cycle - loop_opened
            else:
                cycle_duration = loop_closed - loop_opened
            repeat_cycle = max(math.floor((num_cycles - cycle) / cycle_duration), 0)
            if repeat_cycle == 0:
                board_states[tuple(board)] = (loop_opened, -2)
            else:
                cycle += repeat_cycle * cycle_duration

    return board


@timer_func
def main(filename):
    lines = read_input(filename)
    tilted_lines = tilt_north(lines)
    weight = count_weight(tilted_lines)

    tilted_rotated = rotate_and_tilt_cycle(lines, 1000000000)
    tilted_weight = count_weight(tilted_rotated)

    print(f"Total weight on north side: {weight}")
    print(f"Total weight after rotations: {tilted_weight}")


# main("example.txt")
main("data.txt")
