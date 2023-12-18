import time
import copy
from functools import wraps
import numpy as np


def explore_arrangements_cache_decorator(func):
    cache = {}

    @wraps(func)
    def wrapper(springs, counts):
        # Convert counts list to tuple for hashing
        key = (springs, tuple(counts))

        if key not in cache:
            result = func(springs, counts)
            cache[key] = result
        else:
            result = cache[key]

        return result

    return wrapper


def get_num_damaged(springs):
    counter = 0
    while counter < len(springs) and springs[counter] == "#":
        counter += 1
    return counter


def copy_and_replace_at_begin(sprigs, char):
    new_springs = copy.deepcopy(sprigs)
    new_springs = char + new_springs[1:]
    return new_springs


def try_place_damaged(springs, previous_damaged, counts):
    missing_count = counts[0] - previous_damaged
    while len(springs) > 0 and ((springs[0] == "?" and missing_count > 0) or springs[0] == "#"):
        springs = springs[1:]
        missing_count -= 1

    success = missing_count == 0
    if success and len(springs) > 0:
        springs = springs[1:]
    return success, springs


def explore_questionmark(springs, counts):
    # replace "?" with "."
    point_spring = copy_and_replace_at_begin(springs, ".")
    counter = explore_arrangements(point_spring, counts)

    # replace "?" with "#"
    damaged_spring = copy_and_replace_at_begin(springs, "#")
    counter += explore_arrangements(damaged_spring, counts)
    return counter


def check_whether_no_counts_valid(springs):
    # ensure that there is no further "#" in the line, in this case the config is illegal
    next_damaged = springs.find("#")
    return next_damaged == -1


@explore_arrangements_cache_decorator
def explore_arrangements(springs, counts) -> int:
    num_damaged = 0
    local_counts = copy.deepcopy(counts)
    while len(springs) > 0 and springs[0] != "?":
        if springs[0] == ".":
            if num_damaged != 0:
                if num_damaged == local_counts[0]:
                    local_counts.pop(0)
                    num_damaged == 0
                else:
                    return 0
            springs = springs[1:]

        else:
            num_damaged = get_num_damaged(springs)
            springs = springs[num_damaged:]
            # known damages are already identical to next count of damaged goods
            if num_damaged > local_counts[0]:
                # illegal, therefore no valid arrangement
                return 0
            elif num_damaged == local_counts[0]:
                local_counts.pop(0)

                # check whether is finished now
                if len(local_counts) == 0:
                    return check_whether_no_counts_valid(springs)
                elif len(springs) == 0:
                    # illegal config, no further springs available but counts not empty
                    return 0

                # after successful "#" has to be a ".", therefore no branching here, symbols can only be "." or "?"
                springs = springs[1:]
                num_damaged = 0

    # ensure that there are enough potential damaged springs to fulfill local counts
    num_pot_damaged = springs.count("#") + springs.count("?") + num_damaged
    if num_pot_damaged < sum(local_counts):
        return 0

    # here symbol can only be "?"
    if num_damaged != 0:
        # found a non finished sequence of damaged springs
        success, springs = try_place_damaged(springs, num_damaged, local_counts)
        if not success:
            return 0
        else:
            local_counts.pop(0)
            if len(local_counts) == 0:
                return check_whether_no_counts_valid(springs)

    if len(springs) == 0:
        return len(local_counts) == 0
    if springs[0] == "?":
        counter = explore_questionmark(springs, local_counts)
    else:
        # questionmark was potentially overridden due to num_damaged != 0 and
        # therefore no exploration in this step necessary
        counter = explore_arrangements(springs, local_counts)
    return counter


def count_arrangements(line):
    springs, counts = line.split(" ")
    counts = list(map(int, counts.split(",")))
    num_arrangements = explore_arrangements(springs, counts)
    return num_arrangements


def unfold_line_and_count(line):
    springs, counts = line.split(" ")
    unfolded_springs = springs
    counts = list(map(int, counts.split(",")))
    unfolded_counts = counts
    for i in range(4):
        unfolded_springs = unfolded_springs + "?" + copy.deepcopy(springs)
        unfolded_counts = unfolded_counts + copy.deepcopy(counts)
    num_arrangements = explore_arrangements(unfolded_springs, unfolded_counts)
    return num_arrangements


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

total_num_folded = 0
total_num_unfolded = 0
for line in lines:
    total_num_folded += count_arrangements(line)
    total_num_unfolded += unfold_line_and_count(line)

print(f"Total num of folded arrangements is: {total_num_folded}")
print(f"Total num of unfolded arrangements is: {total_num_unfolded}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
