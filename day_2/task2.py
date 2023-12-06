import numpy as np


# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()


def compute_num_cubes(line):
    line = line.replace("\n", "")
    bag = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    split_line = line.split(": ")
    game_id = int(split_line[0].split(" ")[1])
    rounds = split_line[1].split("; ")
    for round in rounds:
        reveals = round.split(", ")
        for reveal in reveals:
            reveal_part = reveal.split(" ")
            bag[reveal_part[1]] = max(bag[reveal_part[1]], int(reveal_part[0]))
    return bag


total = 0
for line in lines:
    bag = compute_num_cubes(line)
    power_of_bag = np.prod(list(bag.values()))
    total += power_of_bag

print(total)