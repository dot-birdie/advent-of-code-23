import time


def count_pos_arrangements(line):
    springs, counts = line.split(" ")
    counts = list(map(int, counts.split(",")))
    num_arrangements = 0
    return num_arrangements


start_time = time.time()

f = open("example.txt", "r")
# f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

total_num = 0
for line in lines:
    total_num += count_pos_arrangements(line)

print(f"Total num of arrangements is: {total_num}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
