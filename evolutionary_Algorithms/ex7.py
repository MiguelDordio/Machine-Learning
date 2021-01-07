import random
import numpy as np
import matplotlib.pyplot as plt
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


def population_evaluation(population):
    evaluations = []
    for i in population:
        evaluations.append(evaluate_pattern(i))
    return evaluations


# get the best 30% of the population
def get_top_30(population, evaluations):
    top_30 = int((len(population) * 30) / 100)
    top_30_idx = np.argsort(evaluations)[-top_30:]
    return [population[i] for i in top_30_idx]


# ex4 b)
def mutation(pattern):
    pos = random.randint(0, len(pattern)-1)
    bit = pattern[pos]
    if bit == "1":
        pattern = pattern[:pos] + "0" + pattern[pos + 1:]
    else:
        pattern = pattern[:pos] + "1" + pattern[pos + 1:]
    return pattern


# generate the initial population randomly
def random_population(pop_size, pattern_size):
    patterns = []
    for i in range(pop_size):
        patterns.append(random_pattern(pattern_size))
    return patterns


# given the best 30%, generate a population using mutation from them
def generation(top_patterns, pop_size):
    patterns = []
    while len(patterns) < pop_size:
        p1_pos = random.randint(0, len(top_patterns) - 1)
        p2_pos = p1_pos + 1
        if p1_pos == len(top_patterns) - 1:
            p2_pos = 0
        patterns.append(mutation(crossover3(top_patterns[p1_pos], top_patterns[p2_pos])))
    return patterns


# randomly combine half of a pattern with half of another
def crossover(p1, p2):
    p1_parts = [p1[:len(p1) // 2], p1[len(p1) // 2:]]
    p2_parts = [p2[:len(p2) // 2], p2[len(p2) // 2:]]

    part1 = random.randint(0, 1)
    part2 = random.randint(0, 1)

    return p1_parts[part1] + p2_parts[part2]


# randomly pick from each parent half of it`s bits
def crossover2(p1, p2):
    bits1 = []
    while len(bits1) < len(p1) // 2:
        pos = random.randint(0, len(p1)-1)
        if bits1.count(pos) == 0:
            bits1.append(pos)

    bits2 = []
    while len(bits2) < len(p2) // 2:
        pos = random.randint(0, len(p2)-1)
        if bits2.count(pos) == 0:
            bits2.append(pos)

    part1 = ""
    for i in bits1:
        part1 += p1[i]

    part2 = ""
    for i in bits2:
        part2 += p2[i]

    return part1 + part2


def crossover3(p1, p2):
    kid = ""
    pos = random.randint(0, len(p1)-1)
    for i in range(pos):
        kid += p1[i]

    for i in range(pos, len(p2)):
        kid += p2[i]

    return kid


def executor(population_size, pattern_size):
    gens_count = 0
    # initialize random population
    pop = random_population(population_size, pattern_size)
    while True:
        # evaluate population
        pop_evals = population_evaluation(pop)
        # check if it reaches the desired state
        if max(pop_evals) >= 1:
            # print_pattern(pop[pop_evals.index(max(pop_evals))])
            return gens_count
        # get top 30% of the population
        top = get_top_30(pop, pop_evals)
        # generate the next generation based of the top 30%
        pop = generation(top, population_size)
        gens_count += 1


def trials_executor(population_size, sizes, show_run_times):
    colors = ['blue', 'green', 'red', 'orange', 'brown', 'purple']
    c = 0
    all_run_times = []
    for size in sizes:
        trials = 0
        generations = []
        run_times = []
        while trials < 30:
            random.seed(trials)
            start = timeit.default_timer()
            generations.append(executor(population_size, size))
            end = timeit.default_timer()
            run_times.append(end - start)
            trials += 1
        all_run_times.append(run_times)
        print("Test for pattern size:", size, "completed")
        if not show_run_times:
            plot_chart(generations, population_size, colors[c])
        c += 1
    if show_run_times:
        print("Run times:\n", all_run_times)
        plot_boxplot(all_run_times, population_size)
    plt.show()


def plot_chart(epochs, population_size, color):
    plt.suptitle('Generations to find the objective')
    plt.title(' Population size=' + str(population_size))
    plt.ylabel('Generations')
    plt.xlabel('Experiments')
    plt.plot([a for a in range(30)], epochs, c=color, alpha=1, marker='.', )


def plot_boxplot(times, population_size):
    plt.suptitle('Run times to find the objective')
    plt.title(' Population size=' + str(population_size))
    plt.ylabel('Run times')
    plt.boxplot(times)


if __name__ == '__main__':
    # size: 8, 16, 32, 64, 128, 256 bits
    trials_executor(population_size=100, sizes=[8, 16, 32, 64, 128, 256], show_run_times=False)
