import numpy as np
import math
from util_functions import timer_func, read_input

directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}


def model_encounter(lines, position, beam_direction):
    character = lines[position[0]][position[1]]
    if character == "|" and beam_direction[1] != 0:
        return [directions["up"], directions["down"]]
    elif character == "-" and beam_direction[0] != 0:
        return [directions["left"], directions["right"]]
    elif character == "\\":
        return [(beam_direction[1], beam_direction[0])]
    elif character == "/":
        return [(-1 * beam_direction[1], -1 * beam_direction[0])]
    else:
        # default case for ".", and when light direction hits pointy end of splitters "|" and "-"
        return [beam_direction]


def energize_position(field, position, direction):
    field_set = field[position[0]][position[1]]
    if direction not in field_set:
        field_set.append(direction)
        return True
    else:
        return False


def find_energize_for_start_pos(lines, start_pos, start_dir):
    beams = [(start_pos, start_dir)]
    energized_field = [[[] for j in range(len(lines[0]))] for i in range(len(lines))]
    while len(beams) != 0:
        current_beam = beams.pop(0)
        current_pos, current_dir = current_beam
        if not energize_position(energized_field, current_pos, current_dir):
            continue
        beams_after_encounter = model_encounter(lines, current_pos, current_dir)
        for new_beam_dir in beams_after_encounter:
            new_row = current_pos[0] + new_beam_dir[0]
            new_column = current_pos[1] + new_beam_dir[1]
            if 0 <= new_row < len(lines) and 0 <= new_column < len(lines[0]):
                new_pos = (new_row, new_column)
                beams.append((new_pos, new_beam_dir))

    total_energized = 0
    visual_rep_energized = []
    for line_index in range(len(energized_field)):
        visual_rep_energized.append("")
        num_energized = len(list(filter(lambda item: len(item) != 0, energized_field[line_index])))
        for index in range(len(lines[line_index])):
            if len(energized_field[line_index][index]) != 0:
                visual_rep_energized[-1] = visual_rep_energized[-1] + "#"
            else:
                visual_rep_energized[-1] = visual_rep_energized[-1] + "."
        total_energized += num_energized
    return total_energized


def get_max_energy(lines):
    max_energy = 0
    # top & bottom
    for i in range(len(lines[0])):
        max_energy = max(max_energy, find_energize_for_start_pos(lines, (0, i), directions["down"]))
        max_energy = max(max_energy, find_energize_for_start_pos(lines, (len(lines) - 1, i), directions["up"]))
    # left & right
    for i in range(len(lines)):
        max_energy = max(max_energy, find_energize_for_start_pos(lines, (i, 0), directions["right"]))
        max_energy = max(max_energy, find_energize_for_start_pos(lines, (i, len(lines[0]) - 1), directions["left"]))
    return max_energy


@timer_func
def main(filename):
    lines = read_input(filename)
    task_1_energy = find_energize_for_start_pos(lines, (0, 0), directions["right"])
    max_total_energy = get_max_energy(lines)

    print(f"Total num energized is: {task_1_energy}")
    print(f"Overall max energy: {max_total_energy}")


# main("example.txt")
main("data.txt")
