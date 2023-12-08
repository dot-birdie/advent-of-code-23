import time
import math

def extract_mapping(lines) -> dict:
    nodes = {}
    for line in lines:
        line = line.replace("(", "")
        line = line.replace(")", "")
        node, options = line.split(" = ")
        left, right = options.split(", ")
        nodes[node] = (left, right)
    return nodes


def ends_with(element, character):
    return element[-1] == character


def are_all_nodes_final(nodes):
    end_character = "Z"
    non_final_nodes = list(filter(lambda node: not ends_with(node, end_character), nodes))
    return len(non_final_nodes) == 0

start_time = time.time()

# f = open("example.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

instructions = lines[0]
print(f"Num LR instructions: {len(instructions)}")
nodes = extract_mapping(lines[2:])

periods = []
start_character = "A"
current_nodes = list(filter(lambda node: ends_with(node, start_character), nodes.keys()))
print(f"Starting nodes: {current_nodes}")

for node in current_nodes:
    num_steps = 0
    current_node = node
    while not ends_with(current_node, "Z"):
        direction = instructions[num_steps % len(instructions)]
        if direction == "L":
            current_node = nodes[current_node][0]
        else:
            current_node = nodes[current_node][1]
        num_steps += 1

    periods.append(num_steps)

print(f"Periods: {periods}")

lcm = math.lcm(*periods)

print(f"LCM for periods is: {lcm}")

# print(f"Num steps to reach goal node: {num_steps}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
