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


def random_pattern(size):
    pattern = ""
    options = ["0", "1"]
    for i in range(size):
        bite = random.choice(options)
        pattern = pattern + bite
    return pattern


# ex3 compares both pattern char by char and evaluates between 0-100%
def evaluate_pattern(p1, p2):
    counter = 0
    for x, y in zip(p1, p2):
        if x == y:
            counter += 1
    return (counter * 100 / len(p2)) / 100


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
        new_score = evaluate_pattern(new_pattern, find)
        if new_pattern == find:
            return times
        if new_score > score:
            score = new_score
            pattern = new_pattern
        times += 1

def trials_executor(size):
    trials = 0
    time_results = []
    run_times = []
    while trials < 30:
        random.seed(trials)
        start = timeit.default_timer()
        find = random_pattern(size)
        pattern = find
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


