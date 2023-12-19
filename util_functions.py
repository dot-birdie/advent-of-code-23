from time import time


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Program executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


def read_input(filename):
    f = open(filename, "r")
    lines = f.readlines()
    lines = list(map(lambda x: x.replace("\n", ""), lines))
    return lines
