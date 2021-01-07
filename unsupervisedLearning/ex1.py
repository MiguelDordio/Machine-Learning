import numpy as np
import timeit
import copy
import matplotlib.pyplot as plt


def import_file(filename):
    d = np.genfromtxt(fname=filename)
    return d[0], d[1]


def get_coordinates(x_values, y_values):
    coordinates = []
    for x, y in zip(x_values, y_values):
        coordinates.append((x, y))
    return coordinates


def show_chart():
    x_values, y_values = import_file(f_name)
    data_set = get_coordinates(x_values, y_values)
    plot_charts(x_values, y_values)


def plot_charts(x_values, y_values):
    plt.suptitle('Data set')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.scatter(x_values, y_values, c='blue', alpha=1, marker='x')
    # plt.scatter(r2_x_val, r2_y_val, c='red', alpha=1, marker='x')
    plt.show()


if __name__ == '__main__':
    f_name = 'unsupervisedLearningDataSet.txt'
    show_chart()
