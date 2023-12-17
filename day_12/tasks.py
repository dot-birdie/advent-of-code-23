import time
import copy


def get_num_damaged(springs, start_index):
    counter = 0
    while start_index + counter < len(springs) and springs[start_index + counter] == "#":
        counter += 1
    return counter


def copy_and_replace_index(sprigs, index, char):
    new_springs = copy.deepcopy(sprigs)
    new_springs = new_springs[:index] + char + new_springs[index + 1:]
    return new_springs


def explore_arrangements(springs, counts, index, init_damaged) -> int:
    num_damaged = init_damaged
    local_counts = copy.deepcopy(counts)
    while index < len(springs) and springs[index] != "?":
        if springs[index] == ".":
            if num_damaged != 0:
                if num_damaged == local_counts[0]:
                    local_counts.pop(0)
                    num_damaged == 0
                else:
                    return 0
            index += 1

        else:
            newly_found_damaged = get_num_damaged(springs, index)
            num_damaged = num_damaged + newly_found_damaged
            index += newly_found_damaged
            # known damages are already identical to next count of damaged goods
            if num_damaged > local_counts[0]:
                # illegal, therefore no valid arrangement
                return 0
            elif num_damaged == local_counts[0]:
                local_counts.pop(0)

                # check whether is finished now
                if len(local_counts) == 0:
                    # ensure that there is no further "#" in the line, in this case the config is illegal
                    next_damaged = springs[index:].find("#")
                    return next_damaged == -1
                elif index >= len(springs):
                    # illegal config, no further springs available but counts not empty
                    return 0

                # ensure that afterwards is "." symbol, current can only be "." or "?" at this point in the program
                # "#" would have incremented counter and is already checked that at least one further symbol is
                # available
                if springs[index] == ".":
                    index += 1
                else:
                    # only possibility is symbol "?", because with "#" counter would have increased and
                    # len is sufficient
                    springs = springs[:index] + "." + springs[index + 1:]
                    index += 1
                num_damaged = 0

    if index == len(springs):
        return len(local_counts) == 0

    # replace "?" with "."
    point_spring = copy_and_replace_index(springs, index, ".")
    counter = explore_arrangements(point_spring, local_counts, index, num_damaged)
    # replace "?" with "#"
    damaged_spring = copy_and_replace_index(springs, index, "#")
    counter += explore_arrangements(damaged_spring, local_counts, index, num_damaged)
    return counter


def count_arrangements(line):
    springs, counts = line.split(" ")
    counts = list(map(int, counts.split(",")))
    num_arrangements = explore_arrangements(springs, counts, 0, 0)
    return num_arrangements


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

total_num = 0
for line in lines:
    total_num += count_arrangements(line)

print(f"Total num of arrangements is: {total_num}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
