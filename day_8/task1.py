import time

def extract_mapping(lines) -> dict:
    nodes = {}
    for line in lines:
        line = line.replace("(", "")
        line = line.replace(")", "")
        node, options = line.split(" = ")
        left, right = options.split(", ")
        nodes[node] = (left, right)
    return nodes

start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

instructions = lines[0]
nodes = extract_mapping(lines[2:])

num_steps = 0
current_node = "AAA"
goal_node = "ZZZ"

while current_node != goal_node:
    direction = instructions[num_steps % len(instructions)]
    if direction == "L":
        current_node = nodes[current_node][0]
    else:
        current_node = nodes[current_node][1]
    num_steps += 1

print(f"Num steps to reach goal node: {num_steps}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")