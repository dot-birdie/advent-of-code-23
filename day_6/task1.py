
def get_numbers_in_line(line):
    line += " "
    numbers = []
    number_start_index = -1
    for index in range(len(line)):
        if line[index].isdigit() and number_start_index == -1:
            number_start_index = index
        elif not line[index].isdigit() and number_start_index != -1:
            number = int(line[number_start_index:index])
            numbers.append(number)
            number_start_index = -1

    return numbers


def parse_input(lines):
    times = get_numbers_in_line(lines[0][5:])
    distances = get_numbers_in_line(lines[1][9:])
    return list(zip(times, distances))


# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

races = parse_input(lines)

total = 1
for time, distance in races:
    number_beat_distance = 0
    for speed in range(time):
        if speed * (time - speed) > distance:
            number_beat_distance += 1
    print(f"Num of boats that beat the distance: {number_beat_distance}")
    total *= number_beat_distance

print(f"Number of ways to beat the record: {total}")

