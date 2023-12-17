

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

total = 0
for line in lines:
    num_matching = get_number_of_winners(line)
    # print(f"Number of matches: {num_matching}")
    if num_matching > 0:
        points = 2 ** (num_matching - 1)
        # print(f"Received number of points: {points}")
        total += points

print(total)