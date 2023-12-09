import time


def all_items_zero(list):
    return all(item == 0 for item in list)


def compute_diff_lists(line):
    numbers = [list(map(int, line.split(" ")))]
    while not all_items_zero(numbers[-1]):
        diff_list = [numbers[-1][index + 1] - numbers[-1][index] for index in range(len(numbers[-1]) - 1)]
        numbers.append(diff_list)
    return numbers


def predict_back(line):
    numbers = compute_diff_lists(line)
    for index in range(len(numbers) - 2, -1, -1):
        numbers[index].append(numbers[index][-1] + numbers[index + 1][-1])
    return numbers[0][-1]


def predict_front(line):
    numbers = compute_diff_lists(line)
    for index in range(len(numbers) - 2, -1, -1):
        numbers[index][:0] = [numbers[index][0] - numbers[index + 1][0]]
    return numbers[0][0]


start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

total_back = 0
total_front = 0
for line in lines:
    number_back = predict_back(line)
    total_back += number_back
    number_front = predict_front(line)
    total_front += number_front

print(f"Sum of back extrapolated values: {total_back}")
print(f"Sum of front extrapolated values: {total_front}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
