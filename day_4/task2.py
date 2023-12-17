

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()

def get_number_of_winners(line):
    line = line.replace("\n", "")
    prefix, numbers = line.split(": ")
    winners_text, own_numbers_text = numbers.split(" | ")
    winner_numbers = winners_text.split(" ")
    winner_numbers = [number for number in winner_numbers if number != ""]
    own_numbers = own_numbers_text.split(" ")
    own_numbers = [number for number in own_numbers if number != ""]

    num_matching = 0
    for number in own_numbers:
        if number in winner_numbers:
            num_matching += 1

    return num_matching

quantities = [1] * len(lines)
for line_index in range(len(lines) - 1):
    num_matching = get_number_of_winners(lines[line_index])

    quantities[line_index + 1: min(len(lines), line_index + num_matching + 1)] = \
        [quantities[index] + quantities[line_index]
         for index in range(line_index + 1, min(len(lines), line_index + num_matching + 1))]

print(quantities)
print(f"Sum of quantities is: {sum(quantities)}")