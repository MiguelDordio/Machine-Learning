import random
import numpy as np
import math
import timeit
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def import_file(filename):
    d = np.genfromtxt(fname=filename)
    return d[0], d[1]


def get_coordinates(x_values, y_values):
    coordinates = []
    for x, y in zip(x_values, y_values):
        coordinates.append((x, y))
    return coordinates


def get_representatives(data_set, size):
    representatives = []
    for i in range(size):
        new = []
        for j in range(size):
            new.append(data_set[random.randint(0, len(data_set))])
        representatives.append(new)
    return representatives


def update_adjacent(x, y, point, representatives):
    #               N        S        E       O       NE       NO      SE        SO
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    # update all four directions
    for i in range(8):
        # using the direction array
        a = x + directions[i][0]
        b = y + directions[i][1]

        # not blocked and valid
        if 0 <= a < len(representatives) and 0 <= b < len(representatives):
            representatives[a][b] = (
                ((1 - (alfa / 2)) * representatives[a][b][0]) + ((alfa / 2) * point[0]),
                ((1 - (alfa / 2)) * representatives[a][b][1]) + ((alfa / 2) * point[1]))


def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node) ** 2, axis=1)
    return dist_2.argmin()


def executor(size):
    random.seed(0)
    x_values, y_values = import_file(f_name)
    data_set = get_coordinates(x_values, y_values)
    representatives = get_representatives(data_set, size)
    colors = ['green', 'red', 'blue']
    c = 0
    snapshots = []
    for epoch in range(301):
        for x in data_set:
            closest = int(closest_node(x, representatives))
            i = closest // size
            j = closest % size
            item = representatives[i][j]
            item_x = float(item[0])
            item_y = float(item[1])
            representatives[closest // size][closest % size] = (((1 - alfa) * item_x) + (alfa * x[0]),
                                                                ((1 - alfa) * item_y) + (alfa * x[1]))
            update_adjacent(i, j, x, representatives)

        if epoch == 100 or epoch == 200 or epoch == 300:
            color = colors[c]
            c += 1
            a = []
            b = []
            for x in range(size):
                for y in range(size):
                    a.append(representatives[x][y][0])
                    b.append(representatives[x][y][1])
            snapshots.append(plt.scatter(a, b, c=color, alpha=1, marker='.', label=str(epoch) + ' epochs'))
            print("snapshot taken")
    font_p = FontProperties()
    font_p.set_size('xx-small')
    plt.suptitle('Progress of the self-organizing-map')
    plt.title('Alfa=' + str(alfa) + ' Size=' + str(size) + 'x' + str(size))
    plt.ylabel('y')
    plt.xlabel('x')
    plt.legend(handles=snapshots, title='Values', bbox_to_anchor=(1.05, 1), loc='lower center', prop=font_p)
    plt.show()


def runner(size):
    trials = 0
    results = []
    run_times = []
    while trials < 30:
        random.seed(trials)
        start = timeit.default_timer()
        results.append(executor(size))
        end = timeit.default_timer()
        run_times.append(end - start)
        trials += 1


if __name__ == '__main__':
    f_name = 'unsupervisedLearningDataSet.txt'
    alfa = 10e-6
    # runner(alfa)
    executor(10)
