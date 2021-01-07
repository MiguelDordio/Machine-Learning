import random
import itertools
import math


def rule(combination):
    if combination.count('1') >= 6:
        return 1
    else:
        return 0


def initialize_sets():
    raw_data = ["".join(seq) for seq in itertools.product("01", repeat=10)]
    data_set = [(i, rule(i)) for i in raw_data]
    training_set = []
    example_set = []
    training_set_size = (70 * len(data_set)) // 100
    counter = 0
    while len(data_set) > 0:
        # random.seed(counter)
        pos = random.randint(0, len(data_set) - 1)
        if counter < training_set_size:
            training_set.append(data_set[pos])
            counter += 1
        else:
            example_set.append(data_set[pos])
        data_set.remove(data_set[pos])
    return training_set, example_set


def mean(labels):
    return sum(labels) / len(labels)


def mode(labels):
    return max(set(labels), key=labels.count)


def euclidean_distance(a, b):
    sum_sqrt_distance = 0
    for i, j in zip(a, b):
        sum_sqrt_distance += math.pow(int(i) - int(j), 2)
    return math.sqrt(sum_sqrt_distance)


def knn_algorithm(data, query, k, distance_fn, choice_fn):
    neighbours_distances_indices = []
    # for each example in the data
    for index, item in enumerate(data):
        # calculate the distance between the current and the query
        distance = distance_fn(item[0], query[0])

        # add the distance and index to an ordered collection
        neighbours_distances_indices.append((distance, index))

    # sort the ordered collection of distances and indices from smallest to largest
    sorted_distances_indices = sorted(neighbours_distances_indices)

    # pick the first k entries
    k_distances_indices = sorted_distances_indices[:k]

    # get the labels from the selected k entries
    k_neighbours_labels = [data[i][1] for distance, i in k_distances_indices]

    # apply chosen function to calculate the prediction
    return k_neighbours_labels, choice_fn(k_neighbours_labels)


def main(choice_fn):

    k_values = [3, 7, 11]

    for k in k_values:
        random.seed(k)
        training_set, testing_set = initialize_sets()
        print("\nUsing:", choice_fn.__name__, "And k =", k)
        correct_predictions = 0
        for query in testing_set:
            k_neighbours_labels, prediction = knn_algorithm(training_set, query, k=k,
                                                            distance_fn=euclidean_distance, choice_fn=choice_fn)
            # check if prediction was correct
            if prediction == query[1]:
                correct_predictions += 1

        print("Testing set had:", len(testing_set), "and there were", correct_predictions, "correct predictions")


if __name__ == '__main__':
    main(choice_fn=mode)
