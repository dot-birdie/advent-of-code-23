import math


def get_number_in_line(line):
    line = line.replace(" ", "")
    return int(line)


def parse_input(lines):
    time = get_number_in_line(lines[0][5:])
    distance = get_number_in_line(lines[1][9:])
    return time, distance


def pq_formula(time, distance):
    p = -time
    q = distance
    root = math.sqrt((p / 2) ** 2 - q)
    first_term = -p / 2
    return first_term - root, first_term + root


def compute_distance(time, waiting_time):
    return (time - waiting_time) * waiting_time


def find_left_solving(intersection, time, distance):
    waiting_time = math.floor(intersection)
    while compute_distance(time, waiting_time) < distance:
        waiting_time += 1
    return waiting_time


def find_right_solving(intersection, time, distance):
    waiting_time = math.ceil(intersection)
    while compute_distance(time, waiting_time) < distance:
        waiting_time -= 1
    return waiting_time


# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

time, distance = parse_input(lines)
intersection_left, intersection_right = pq_formula(time, distance)
waiting_left = find_left_solving(intersection_left, time, distance)
waiting_right = find_right_solving(intersection_right, time, distance)

num_solving_possibilities = waiting_right - waiting_left + 1
print(f"Number of ways to beat the record: {num_solving_possibilities}")
