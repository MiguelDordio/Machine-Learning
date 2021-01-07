import random
import timeit


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
    for i in range(3):
        pos = random.randint(0, len(pattern)-1)
        bit = pattern[pos]
        if bit == "1":
            pattern = pattern[:pos] + "0" + pattern[pos + 1:]
        else:
            pattern = pattern[:pos] + "1" + pattern[pos + 1:]
    return pattern


def executor(pattern, find):
    times = 0
    score = 0
    while True:
        new_pattern = mutation(pattern)
        new_score = evaluate_pattern(new_pattern)
        if new_pattern == find:
            return times
        if new_score > score:
            score = new_score
            pattern = new_pattern
        times += 1


def trials_executor(size):
    find = ""
    for i in range(size):
        find += "0"
    trials = 0
    time_results = []
    run_times = []
    while trials < 30:
        random.seed(trials)
        start = timeit.default_timer()
        pattern = random_pattern(size)
        time_results.append(executor(pattern, find))
        end = timeit.default_timer()
        run_times.append(end - start)
        trials += 1
    for i in time_results:
        print(i)
    print("tempos")
    for i in run_times:
        print("{:.8f}".format(float(i)).replace('.', ','))


if __name__ == '__main__':
    # size: 8, 16, 32, 64, 128, 256 bits
    trials_executor(size=8)


