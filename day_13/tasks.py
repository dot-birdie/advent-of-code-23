import time
import numpy as np


def transpose_patch(patch):
    new_patch = ["" for i in range(len(patch[0]))]
    for i in range(len(patch[0])):
        for j in range(len(patch)):
            new_patch[i] = new_patch[i] + patch[j][i]
    return new_patch


def get_vertical_score(patch, clean_value=-2):
    transposed = transpose_patch(patch)
    split = get_horizontal_score(transposed, clean_value, True)
    return split


def get_horizontal_score(patch, clean_value=-2, is_from_vertical=False):
    for i in range(1, len(patch)):
        top = patch[:i]
        top.reverse()
        bottom = patch[i:]
        if len(top) > len(bottom):
            top = top[:len(bottom)]
        else:
            bottom = bottom[:len(top)]
        new_score = i * ((not is_from_vertical) * 100 + is_from_vertical)
        if top == bottom and new_score != clean_value:
            return new_score
    return -1


def get_value_for_patch(patch, clean_value=-2):
    vertical = get_vertical_score(patch, clean_value)
    horizontal = get_horizontal_score(patch, clean_value)
    if vertical != -1:
        return vertical
    elif horizontal != -1:
        return horizontal
    return -1


def get_dirty_value(patch, clean_value):
    flip_dict = {
        "#": ".",
        ".": "#"
    }

    for i in range(len(patch)):
        for j in range(len(patch[0])):
            patch[i] = patch[i][:j] + flip_dict[patch[i][j]] + patch[i][j + 1:]
            dirty_value = get_value_for_patch(patch, clean_value)
            if dirty_value != -1:
                return dirty_value
            else:
                patch[i] = patch[i][:j] + flip_dict[patch[i][j]] + patch[i][j + 1:]


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))
patches = [[]]

for line in lines:
    if line != "":
        patches[-1].append(line)
    else:
        patches.append([])

total_clean = 0
total_dirty = 0
for patch in patches:
    clean_value = get_value_for_patch(patch)
    total_clean += clean_value
    total_dirty += get_dirty_value(patch, clean_value)

print(f"Total after summarizing: {total_clean}")
print(f"Total for dirty variant: {total_dirty}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
