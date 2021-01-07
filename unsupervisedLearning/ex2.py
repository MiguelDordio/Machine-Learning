import random
import math
import numpy as np
import timeit
import copy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import statistics as st


def import_file(filename):
    d = np.genfromtxt(fname=filename)
    return d[0], d[1]


def get_coordinates(x_values, y_values):
    coordinates = []
    for x, y in zip(x_values, y_values):
        coordinates.append((x, y))
    return coordinates


# Exercise 2 a)
def executor(data_set):
    r1 = data_set[random.randint(0, len(data_set))]
    r2 = data_set[random.randint(0, len(data_set))]
    r1_values = [copy.deepcopy(r1)]
    r2_values = [copy.deepcopy(r2)]
    for counter in range(10):
        for x in data_set:
            # Euclidean distance
            dist_r1 = math.dist(x, r1)
            dist_r2 = math.dist(x, r2)
            if dist_r1 < dist_r2:
                r1 = (((1 - alfa) * r1[0]) + (alfa * x[0]), ((1 - alfa) * r1[1]) + (alfa * x[1]))
            elif dist_r2 < dist_r1:
                r2 = (((1 - alfa) * r2[0]) + (alfa * x[0]), ((1 - alfa) * r2[1]) + (alfa * x[1]))
        print(r1)
        print(r2)
        r1_values.append(r1)
        r2_values.append(r2)
    return r1_values, r2_values, r1, r2


# Exercise 2 b)
def executor2(data_set):
    r1 = data_set[random.randint(0, len(data_set))]
    r2 = data_set[random.randint(0, len(data_set))]
    r1_values = [copy.deepcopy(r1)]
    r2_values = [copy.deepcopy(r2)]
    for counter in range(10):
        counter_r1 = 0
        counter_r2 = 0
        d1 = (0, 0)
        d2 = (0, 0)
        for x in data_set:
            dist_r1 = math.dist(x, r1)
            dist_r2 = math.dist(x, r2)
            if dist_r1 < dist_r2:
                d1 = ((d1[0] + (x[0] - r1[0])), (d1[1] + (x[1] - r1[1])))
                counter_r1 += 1
            elif dist_r2 < dist_r1:
                d2 = ((d2[0] + (x[0] - r2[0])), (d2[1] + (x[1] - r2[1])))
                counter_r2 += 1
        r1 = ((r1[0] + ((alfa / counter_r1) * d1[0])), (r1[1] + (alfa / counter_r1) * d1[1]))
        r2 = ((r2[0] + ((alfa / counter_r2) * d2[0])), (r2[1] + (alfa / counter_r2) * d2[1]))
        print(r1)
        print(r2)
        r1_values.append(r1)
        r2_values.append(r2)
    return r1_values, r2_values, r1, r2


def runner(one_time, ex2_a, ex3):
    x_values, y_values = import_file(f_name)
    data_set = get_coordinates(x_values, y_values)
    if one_time:
        random.seed(0)
        if ex2_a:
            r1_values, r2_values, r1, r2 = executor(data_set)
            print(r1_values)
        else:
            r1_values, r2_values, r1, r2 = executor2(data_set)

        if ex3:
            run_ex3(data_set, r1, r2)
        else:
            plot_charts(r1_values, r2_values, True)
    else:
        trials = 0
        r1_std_values = []
        r2_std_values = []
        run_times = []
        while trials < 30:
            print("\n Experiment:", trials, '\n')
            random.seed(trials)
            start = timeit.default_timer()
            if ex2_a:
                r1_values, r2_values, r1, r2 = executor(data_set)
            else:
                r1_values, r2_values, r1, r2 = executor2(data_set)
            r1_std_values.append(std_deviation(r1_values))
            r2_std_values.append(std_deviation(r2_values))
            end = timeit.default_timer()
            run_times.append(end - start)
            trials += 1
        plot_std_chart(r1_std_values, r2_std_values)


def run_ex3(data_set, r1, r2):
    r1_neighbours = []
    r2_neighbours = []
    for x in data_set:
        dist_r1 = math.hypot(r1[0] - x[0], r1[1] - x[1])
        dist_r2 = math.hypot(r2[0] - x[0], r2[1] - x[1])
        if dist_r1 < dist_r2:
            r1_neighbours.append(x)
        elif dist_r2 < dist_r1:
            r2_neighbours.append(x)

    plt.scatter(r1[0], r1[1], c='black', alpha=1, marker='.')
    plt.scatter(r2[0], r2[1], c='white', alpha=1, marker='.')
    plot_charts(r1_neighbours, r2_neighbours, False)


def plot_charts(r1_values, r2_values, labels):
    r1_x_val = [x[0] for x in r1_values]
    r1_y_val = [y[1] for y in r1_values]

    r2_x_val = [x[0] for x in r2_values]
    r2_y_val = [y[1] for y in r2_values]

    if labels:
        for i, txt in enumerate([i for i in range(11)]):
            plt.annotate(txt, (r1_x_val[i], r1_y_val[i]))

        for i, txt in enumerate([i for i in range(11)]):
            plt.annotate(txt, (r2_x_val[i], r2_y_val[i]))

    font_p = FontProperties()
    font_p.set_size('xx-small')
    plt.suptitle('Progress of r1 and r2 values')
    plt.title('Alfa= ' + str(alfa))
    plt.ylabel('y')
    plt.xlabel('x')
    p1 = plt.scatter(r1_x_val, r1_y_val, c='green', alpha=1, marker='.', label='r1 values')
    p2 = plt.scatter(r2_x_val, r2_y_val, c='red', alpha=1, marker='.', label='r2 values')
    plt.legend(handles=[p1, p2], title='Values', bbox_to_anchor=(1.05, 1), loc='lower center', prop=font_p)
    plt.show()


def std_deviation(values):
    x_values = [i[0] for i in values]
    y_values = [i[1] for i in values]

    return math.sqrt(math.pow(st.stdev(x_values), 2) + math.pow(st.stdev(y_values), 2))


def plot_std_chart(r1_std_values, r2_std_values):
    font_p = FontProperties()
    font_p.set_size('xx-small')
    plt.suptitle('Standard deviation of r1 and r2 values')
    plt.title('Alfa= ' + str(alfa))
    plt.ylabel('Standard deviation')
    plt.xlabel('r1: σ={:.4f} | r2: σ={:.4f}'.format(st.pstdev(r1_std_values), st.pstdev(r2_std_values)))
    p1 = plt.scatter([i for i in range(30)], r1_std_values, c='green', alpha=1, marker='.', label='r1 values')
    p2 = plt.scatter([i for i in range(30)], r2_std_values, c='red', alpha=1, marker='.', label='r2 values')
    plt.legend(handles=[p1, p2], title='Values', bbox_to_anchor=(1.05, 1), loc='lower center', prop=font_p)
    plt.show()


if __name__ == '__main__':
    f_name = 'unsupervisedLearningDataSet.txt'
    alfa = 0.9
    runner(one_time=False, ex2_a=False, ex3=False)
