import itertools
from collections import Counter
import math


def rule(combination):
    if combination.count('1') >= 6:
        return 1
    else:
        return 0


def get_two_subsets(data_set, column):
    sub_set1 = []
    sub_set2 = []
    for item in data_set:
        bit = int(item[0][column])
        if bit == 1:
            sub_set1.append(item)
        else:
            sub_set2.append(item)
    return sub_set1, sub_set2


def entropy(data):
    c = Counter(elem[1] for elem in data)
    probabilities = []
    for key, val in c.items():
        probabilities.append((val * 1) / len(data))

    return - probabilities[0] * math.log(probabilities[0], 2) - probabilities[1] * math.log(probabilities[1], 2)


def gain(data, sub_set1, sub_set2, feature):
    # G(S, a) = entropy(S) − ∑(| Sv | Entropy(Sv)) / | S |
    g = entropy(data) - ((len(sub_set1) * entropy(sub_set1)) + (len(sub_set2) * entropy(sub_set2))) / len(data)
    return round(g, 3), feature


def main():
    raw_data = ["".join(seq) for seq in itertools.product("01", repeat=10)]
    data_set = [(i, rule(i)) for i in raw_data]

    sub_set1_entropy = []
    sub_set2_entropy = []
    gains = []

    # for each feature
    for i in range(len(data_set[0][0])):
        sub_set1, sub_set2 = get_two_subsets(data_set, i)
        sub_set1_entropy.append(round(entropy(sub_set1), 3))
        sub_set2_entropy.append(round(entropy(sub_set2), 3))
        gains.append(gain(data_set, sub_set1, sub_set2, i))

    print("Data set entropy:", entropy(data_set))
    print("Sub set 1 entropy:", sub_set1_entropy)
    print("Sub set 2 entropy:", sub_set2_entropy)
    print("Gains:", gains)


if __name__ == '__main__':
    main()
