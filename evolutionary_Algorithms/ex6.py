import random
import numpy as np
import timeit
import matplotlib.pyplot as plt


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
        evaluations.append(round(evaluate_pattern(i), 2))
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
    patterns = top_patterns
    i = 0
    iter_size = len(top_patterns)
    max_rotations = (pop_size // iter_size) - 1
    rotation = 0
    extra_round = pop_size % iter_size
    while True:
        patterns.append(mutation(top_patterns[i]))
        i += 1
        if rotation < max_rotations:
            if i == iter_size:
                i = 0
                rotation += 1
        else:
            if i == extra_round:
                break
    return patterns


def generation2(top_patterns, pop_size):
    patterns = []
    while len(patterns) < pop_size:
        pos = random.randint(0, len(top_patterns) - 1)
        patterns.append(mutation(top_patterns[pos]))
    return patterns


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
    trials_executor(population_size=100, sizes=[8, 16, 32, 64, 128, 256], show_run_times=True)


