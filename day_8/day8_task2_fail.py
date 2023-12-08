# would work but significantly too slow for the puzzle input
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


def ends_with(element, character):
    return element[-1] == character


def are_all_nodes_final(nodes):
    end_character = "Z"
    non_final_nodes = list(filter(lambda node: not ends_with(node, end_character), nodes))
    return len(non_final_nodes) == 0


start_time = time.time()

# f = open("example2.txt", "r")
f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))

instructions = lines[0]
nodes = extract_mapping(lines[2:])

num_steps = 0
start_character = "A"
current_nodes = list(filter(lambda node: ends_with(node, start_character), nodes.keys()))
print(f"Starting nodes: {current_nodes}")

while not are_all_nodes_final(current_nodes):
    direction = instructions[num_steps % len(instructions)]
    if direction == "L":
        dst_index = 0
    else:
        dst_index = 1

    for index in range(len(current_nodes)):
        current_nodes[index] = nodes[current_nodes[index]][dst_index]

    num_steps += 1
    if num_steps % 500000 == 0:
        print(f"Round num: {num_steps}, num nodes currently: {len(current_nodes)}")


print(f"Num steps to reach goal node: {num_steps}")
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
