



f = open("data.txt", "r")
lines = f.readlines()

total = 0
for line in lines:
    digits = list(filter(str.isdigit, line))
    number = int(digits[0] + digits[-1])
    total += number

print(total)
