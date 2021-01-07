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


# ex1
def random_pattern(size):
    pattern = ""
    options = ["0", "1"]
    for i in range(size):
        bite = random.choice(options)
        pattern = pattern + bite
    return pattern


def executor(size, pattern):
    times = 0
    while True:
        new_pattern = random_pattern(size)
        if new_pattern == pattern:
            return times
        times += 1


def trials_executor(size):
    trials = 0
    time_results = []
    run_times = []
    while trials < 30:
        random.seed(trials)
        start = timeit.default_timer()
        find = random_pattern(size)
        time_results.append(executor(size, find))
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
    trials_executor(size=16)


