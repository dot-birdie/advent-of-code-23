import re


f = open("data.txt", "r")
# f = open("example.txt", "r")
lines = f.readlines()

numbers_spelled = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

total = 0
for line in lines:
    for index in range(len(line)):
        for number in range(len(numbers_spelled)):
            length = len(numbers_spelled[number])
            if index + length < len(line) and line[index:index+length] == numbers_spelled[number]:
                line = line[:index] + str(number + 1) + line[index+1:]


    # print(line)
    digits = list(filter(str.isdigit, line))
    number = int(digits[0] + digits[-1])
    # print(number)
    total += number

print(total)