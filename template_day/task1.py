import time

start_time = time.time()

f = open("example.txt", "r")
# f = open("data.txt", "r")
lines = f.readlines()
lines = list(map(lambda x: x.replace("\n", ""), lines))


for line in lines:
    pass

end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")