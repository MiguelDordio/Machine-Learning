import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


class Label:
    CLUSTER = 1
    BORDER = 2
    NOISE = 3


UNCLASSIFIED = False
NOISE = None


class Node:
    def __init__(self, position=None, index=None, visited=None):
        self.position = position  # (1, 2)
        self.index = index
        self.visited = visited
        self.label = None
        self.cluster = None

    def __eq__(self, other):
        return self.position[0], self.position[1] == other.position[0], self.position[1]

    def __hash__(self):
        return hash((self.position, self.visited, self.label, self.cluster))

    def __ne__(self, other):
        return not self.__eq__(other)


def import_file(filename):
    d = np.genfromtxt(fname=filename)
    return d[0], d[1]


def get_coordinates(x_values, y_values):
    coordinates = []
    i = 0
    for x, y in zip(x_values, y_values):
        coordinates.append(Node((x, y), i, False))
        i += 1
    return coordinates


def reachable_points(data_set, point, radius):
    points = []
    for i in data_set:
        # euclidean distance
        distance = math.hypot(point.position[0] - i.position[0], point.position[1] - i.position[1])
        if distance <= radius:
            points.append(i)
    return points


def dbscan(eps, min_pts):
    x_values, y_values = import_file(f_name)
    data_set = get_coordinates(x_values, y_values)
    cluster = 1
    labels = [UNCLASSIFIED] * len(data_set)

    for point_id in range(0, len(data_set)):
        p = data_set[point_id]
        if labels[point_id] == UNCLASSIFIED:
            neighbor_points = reachable_points(data_set, p, eps)  # Find neighbors
            if len(neighbor_points) < min_pts:  # Density check
                labels[point_id] = NOISE  # Label as Noise
            else:
                labels[point_id] = cluster
                for seed_id in neighbor_points:
                    labels[seed_id.index] = cluster

                while len(neighbor_points) > 0:
                    current_point = neighbor_points[0]
                    results = reachable_points(data_set, current_point, eps)
                    if len(results) >= min_pts:
                        for i in range(0, len(results)):
                            result_point = results[i]
                            if labels[result_point.index] == UNCLASSIFIED or \
                                    labels[result_point.index] == NOISE:
                                if labels[result_point.index] == UNCLASSIFIED:
                                    neighbor_points.append(result_point)
                                labels[result_point.index] = cluster
                    neighbor_points = neighbor_points[1:]
                cluster += 1

    for i in range(len(labels)):
        data_set[i].cluster = labels[i]

    return data_set, cluster


def plot_res(cluster_res, cluster_num, eps, min_pts):
    font_p = FontProperties()
    font_p.set_size('xx-small')
    labels = []
    scatter_colors = ['black', 'green', 'brown', 'red', 'purple', 'orange', 'yellow']
    print("Number of clusters: ", cluster_num)
    for i in range(1, cluster_num):
        color = scatter_colors[i]
        x = []
        y = []
        counter = 0
        for point in cluster_res:
            if point.cluster == i:
                x.append(point.position[0])
                y.append(point.position[1])
                counter += 1
        print("cluster: ", i, "has ", counter, "items")
        labels.append(plt.scatter(x, y, c=color, alpha=1, marker='.', label='Cluster: ' + str(i)))

    x = []
    y = []
    counter = 0
    for point in cluster_res:
        if point.cluster is None:
            x.append(point.position[0])
            y.append(point.position[1])
            counter += 1
    print("outliers: ", counter)
    plt.suptitle('DBScan Algorithm')
    plt.title('Eps=' + str(eps) + ' MinPts=' + str(min_pts))
    plt.ylabel('y')
    plt.xlabel('x')
    labels.append(plt.scatter(x, y, c='blue', alpha=1, marker='.', label='Noise'))
    plt.legend(handles=labels, title='Values', bbox_to_anchor=(1.05, 1), loc='lower center', prop=font_p)


if __name__ == '__main__':
    f_name = 'unsupervisedLearningDataSet.txt'
    data, clusters = dbscan(0.5, 8)
    plot_res(data, clusters, 0.5, 8)
    plt.show()
