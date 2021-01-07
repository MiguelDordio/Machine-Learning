import random
import itertools
import matplotlib.pyplot as plt
import timeit
import statistics as st


def rule(combination):
    if combination.count(1) >= 6:
        return 1
    else:
        return 0


def apply_rule(ops):
    res = []
    for i in ops:
        res.append(rule(i))
    return res


# algorithm logic to progress
def perceptron(w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, op, errors):
    x = w0 + (op[0] * w1) + (op[1] * w2) + (op[2] * w3) + (op[3] * w4) + (op[4] * w5) + \
        (op[5] * w6) + (op[6] * w7) + (op[7] * w8) + (op[8] * w9) + (op[9] * w10)
    if x > 0:
        res = 1
    else:
        res = 0
    # introducing error in the output
    if errors:
        if add_error():
            return 1 if res == 0 else 0
        else:
            return res
    else:
        return res


def add_error():
    random_options = [False, True]
    random_probabilities = [0.999, 0.001]
    return random.choices(random_options, random_probabilities)[0]


def executor(operator, outcome, alpha, errors):
    # initialize w0, w1 and w2 with small random values
    w0 = random.uniform(-0.1, 0.1)
    w1 = random.uniform(-0.1, 0.1)
    w2 = random.uniform(-0.1, 0.1)
    w3 = random.uniform(-0.1, 0.1)
    w4 = random.uniform(-0.1, 0.1)
    w5 = random.uniform(-0.1, 0.1)
    w6 = random.uniform(-0.1, 0.1)
    w7 = random.uniform(-0.1, 0.1)
    w8 = random.uniform(-0.1, 0.1)
    w9 = random.uniform(-0.1, 0.1)
    w10 = random.uniform(-0.1, 0.1)
    delta_w0 = delta_w1 = delta_w2 = delta_w3 = delta_w4 = delta_w5 = \
        delta_w6 = delta_w7 = delta_w8 = delta_w9 = delta_w10 = epochs = 0
    res = [-1] * len(operator)
    while True:
        for i in range(0, len(operator)):
            res[i] = perceptron(w0, w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, operator[i], errors)
            delta_w0 += alpha * (outcome[i] - res[i])
            delta_w1 += alpha * operator[i][0] * (outcome[i] - res[i])
            delta_w2 += alpha * operator[i][1] * (outcome[i] - res[i])
            delta_w3 += alpha * operator[i][2] * (outcome[i] - res[i])
            delta_w4 += alpha * operator[i][3] * (outcome[i] - res[i])
            delta_w5 += alpha * operator[i][4] * (outcome[i] - res[i])
            delta_w6 += alpha * operator[i][5] * (outcome[i] - res[i])
            delta_w7 += alpha * operator[i][6] * (outcome[i] - res[i])
            delta_w8 += alpha * operator[i][7] * (outcome[i] - res[i])
            delta_w9 += alpha * operator[i][8] * (outcome[i] - res[i])
            delta_w10 += alpha * operator[i][9] * (outcome[i] - res[i])
        w0 += delta_w0
        w1 += delta_w1
        w2 += delta_w2
        w3 += delta_w3
        w4 += delta_w4
        w5 += delta_w5
        w6 += delta_w6
        w7 += delta_w7
        w8 += delta_w8
        w9 += delta_w9
        w10 += delta_w10

        if res == outcome:
            break
        epochs += 1
    return epochs


# to study the results, run the program 30 times and record the average
def test_runner(alphas, errors, show_run_times):
    operators_s = ["".join(seq) for seq in itertools.product("01", repeat=10)]
    operators = []
    for i in operators_s:
        o = []
        for j in i:
            o.append(int(j))
        operators.append(o)
    results_rule = apply_rule(operators)

    print("desired: ", results_rule)
    print("1 counts: ", results_rule.count(1), " | ", round((results_rule.count(1) * 100) / len(results_rule), 2),
          "% - 0 counts: ", results_rule.count(0), " | ",
          round((results_rule.count(0) * 100) / len(results_rule), 2), "%")

    colors = ['green', 'red']
    c = 0

    for alpha in alphas:
        times = 0
        epochs = []
        run_times = []
        while times < 30:
            random.seed(times)
            start = timeit.default_timer()
            epochs.append(executor(operators, results_rule, alpha, errors))
            end = timeit.default_timer()
            run_times.append(end - start)
            times += 1
        if show_run_times:
            plot_boxplot(run_times, alpha)
        plot_chart(epochs, alpha, colors[c], errors)
        c += 1


def plot_chart(epochs, alpha, color, errors):
    plt.suptitle('Epochs to find the Rule')
    plt.title(' Alfa=' + str(alpha) + (' p(error)= 0,01%' if errors else ''))
    plt.ylabel('Epochs')
    plt.xlabel('Experiments')
    plt.plot([a for a in range(30)], epochs, c=color, alpha=1, marker='.', )
    plt.show()


def plot_boxplot(times, alpha):
    plt.suptitle('Run times to find the Rule')
    plt.title(' Alfa=' + str(alpha))
    plt.ylabel('Run times')
    plt.xlabel('μ={:.6f} σ={:.6f}'.format((sum(times) / len(times)), st.pstdev(times)))
    plt.boxplot(times)
    plt.show()


if __name__ == '__main__':
    # error = True -> apply error probability
    # show_run_times = True -> also display run_times boxplot
    test_runner(alphas=[0.1, 0.9], errors=True, show_run_times=False)
