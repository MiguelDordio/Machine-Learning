import random
import time


def print_pattern(pattern):
    p_pattern = ""
    counter = 0
    for i in pattern:
        if counter == 4:
            p_pattern += " "
            counter = 0
        counter += 1
        p_pattern += i
    print(p_pattern)


def format_pattern(pattern):
    p_pattern = ""
    counter = 0
    for i in pattern:
        if counter == 4:
            p_pattern += " "
            counter = 0
        counter += 1
        p_pattern += i
    return p_pattern


# ex1
def random_pattern(size):
    pattern = ""
    options = ["0", "1"]
    for i in range(size):
        bite = random.choice(options)
        pattern = pattern + bite
    return pattern


# ex4 count the number os "0"s
def evaluate_pattern(pattern):
    counter = 0
    for x in pattern:
        if x == "0":
            counter += 1
    return (counter * 100 / len(pattern)) / 100


# ex4 b)
def mutation(pattern):
    pos = random.randint(0, len(pattern)-1)
    bit = pattern[pos]
    if bit == "1":
        pattern = pattern[:pos] + "0" + pattern[pos + 1:]
    else:
        pattern = pattern[:pos] + "1" + pattern[pos + 1:]
    return pattern


def executor(size):
    # pattern = random_pattern(size)
    pattern = ""
    for i in range(size):
        pattern += "1"
    initial_score = evaluate_pattern(pattern)
    times = 0
    while times < 1000:
        random.seed(times)
        new_pattern = mutation(pattern)
        score = evaluate_pattern(new_pattern)
        if score > initial_score:
            initial_score = score
            pattern = new_pattern
        times += 1
    print_pattern(pattern)
    print(evaluate_pattern(pattern) * 100)


if __name__ == '__main__':
    # size: 8, 16, 32, 64, 128, 256 bits
    executor(size=256)


