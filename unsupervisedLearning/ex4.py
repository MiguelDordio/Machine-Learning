import random
import numpy as np
import timeit
from scipy.spatial import distance


def import_file(filename):
    d = np.genfromtxt(fname=filename)
    return d[0], d[1]


def get_coordinates(x_values, y_values):
    coordinates = []
    for x, y in zip(x_values, y_values):
        coordinates.append((x, y))
    return coordinates


def get_representatives(data_set, size):
    return [data_set[random.randint(0, len(data_set) - 1)] for _ in range(size)]


def get_all_distances(data_set):
    return distance.cdist(data_set, data_set, 'euclidean')


def executor(sample_size):
    x_values, y_values = import_file(f_name)
    raw_data_set = get_coordinates(x_values, y_values)
    data_set = get_representatives(raw_data_set, sample_size)
    distances = np.array(get_all_distances(data_set))

    while len(data_set) > 2:
        # obtem lista com todos as distâncias maiores que 0 (exclui distâncias às próprias coordenadas)
        g = distances[distances > 0]
        # obtem a posição na lista de distancias da mais pequena
        # min_pos = divmod(g.argmin(), g)
        min_pos = np.where(distances == g.min())

        # coordenadas mais próximas do data set
        point_a = data_set[min_pos[0][0]]
        point_b = data_set[min_pos[0][1]]

        # novo ponto com as médias dos 2 pontos mais próximos
        new_point = ((point_a[0] + point_b[0]) / 2, (point_a[1] + point_b[1]) / 2)

        # remover os 2 pontos mais próximos do data set e atualizar com a nova combinacao
        data_set.remove(point_a)
        if point_a != point_b:
            data_set.remove(point_b)
        data_set.append(new_point)

        # calcular de novo as distâncias
        distances = np.array(get_all_distances(data_set))

    return [(round(i[0], 3), round(i[1], 3)) for i in data_set]
    # fi = [(round(i[0], 3), round(i[1], 3)) for i in data_set]
    # print(fi)


def test():
    sample_sizes = [100, 500]
    results = []
    for size in sample_sizes:
        random.seed(0)
        results.append(executor(size))
    print(results)


if __name__ == '__main__':
    f_name = 'unsupervisedLearningDataSet.txt'
    test()

