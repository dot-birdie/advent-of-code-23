import time
import numpy as np


def check_vertical_all_dots(lines, column_index):
    all_same = True
    for row_index in range(len(lines)):
        all_same = all_same and lines[row_index][column_index] == "."
    return all_same


def get_vertical_mapping(lines):
    vertical_mapping = {}
    expanded_column_index = 0
    for column_index in range(len(lines[0])):
        vertical_mapping[str(column_index)] = expanded_column_index
        all_same = check_vertical_all_dots(lines, column_index)
        if all_same:
            expanded_column_index += 1000000
        else:
            expanded_column_index += 1
    return vertical_mapping


def expand_and_discover(lines):
    # horizontal automatically during labeling

    galaxies = []
    vertical_mapping = get_vertical_mapping(lines)
    horizontal_index_extended = 0

    for i in range(len(lines)):
        found_galaxy = False
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                galaxies.append(tuple((horizontal_index_extended, vertical_mapping[str(j)])))
                found_galaxy = True
        if found_galaxy:
            horizontal_index_extended += 1
        else:
            horizontal_index_extended += 1000000
    return galaxies


def compute_distance(point_1, point_2):
    return np.sum(np.absolute(np.subtract(point_1, point_2)))


def compute_pairwise_galaxy_distances(galaxies):
    total = 0
    num_pairs = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            total += int(compute_distance(galaxies[i], galaxies[j]))
            num_pairs += 1
    print(f"Num pairs counted: {num_pairs}")
    return total


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

galaxies = expand_and_discover(lines)
print(galaxies)
print(f"Total pairwise distance of galaxies: {compute_pairwise_galaxy_distances(galaxies)}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
