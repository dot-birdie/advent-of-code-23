


f = open("data.txt", "r")
lines = f.readlines()

bag = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def check_line(line):
    line = line.replace("\n", "")
    split_line = line.split(": ")
    game_id = int(split_line[0].split(" ")[1])
    valid_game = True
    rounds = split_line[1].split("; ")
    for round in rounds:
        reveals = round.split(", ")
        for reveal in reveals:
            reveal_part = reveal.split(" ")
            valid_game = valid_game and int(reveal_part[0]) <= bag[reveal_part[1]]
    return game_id, valid_game


total = 0
for line in lines:
    game_id, valid_game = check_line(line)
    if valid_game:
        total += game_id

print(total)