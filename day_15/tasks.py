import numpy as np
import math
from util_functions import timer_func, read_input


def compute_hash(element):
    current = 0
    for character in element:
        current += ord(character)
        current *= 17
        current = current % 256
    return current


def compute_total_hash(line):
    values_to_hash = line.split(",")
    total = 0
    for step in values_to_hash:
        total += compute_hash(step)
    return total


def get_index_of_element(hash_table, box_index, label):
    for i in range(len(hash_table[box_index])):
        if hash_table[box_index][i][0] == label:
            return i
    return -1


def remove_label(hash_table, label):
    box_index = compute_hash(label)
    element_index = get_index_of_element(hash_table, box_index, label)
    if element_index != -1:
        hash_table[box_index] = hash_table[box_index][:element_index] + hash_table[box_index][element_index + 1:]


def insert_lens(hash_table, label, lens):
    box_index = compute_hash(label)
    element_index = get_index_of_element(hash_table, box_index, label)
    if element_index != -1:
        hash_table[box_index][element_index] = (label, lens)
    else:
        hash_table[box_index].append((label, lens))


def fill_hashmap(line):
    hash_map = [[] for i in range(256)]
    labeled_lenses = line.split(",")
    for labeled_lens in labeled_lenses:
        operator_index = max(labeled_lens.find("-"), labeled_lens.find("="))
        label = labeled_lens[:operator_index]
        operation = labeled_lens[operator_index]
        if operation == "-":
            remove_label(hash_map, label)
        else:
            insert_lens(hash_map, label, int(labeled_lens[operator_index + 1]))
    return hash_map


def compute_fusing_power(hash_table):
    total = 0
    for i in range(256):
        for j in range(len(hash_table[i])):
            total += (i + 1) * (j + 1) * hash_table[i][j][1]
    return total


@timer_func
def main(filename):
    lines = read_input(filename)
    filled_hash_map = fill_hashmap(lines[0])

    print(f"Total for the initialization sequence is: {compute_total_hash(lines[0])}")
    print(f"Total focusing power: {compute_fusing_power(filled_hash_map)}")


# main("example.txt")
main("data.txt")
