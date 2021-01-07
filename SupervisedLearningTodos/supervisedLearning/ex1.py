import random
import matplotlib.pyplot as plt
import timeit
import statistics as st

# algorithm logic to progress
def perceptron(w0, w1, w2, x, y):
    x = w0 + (x * w1) + (y * w2)
    if x > 0:
        return 1
    else:
        return 0


def executor(operator, outcome, alpha):
    # initialize w0, w1 and w2 with small random values
    w0 = random.uniform(-0.1, 0.1)
    w1 = random.uniform(-0.1, 0.1)
    w2 = random.uniform(-0.1, 0.1)
    delta_w0 = delta_w1 = delta_w2 = epochs = 0
    res = [-1, -1, -1, -1]
    while True:
        for i in range(0, 4):
            res[i] = perceptron(w0, w1, w2, operator[i][0], operator[i][1])
            delta_w0 += alpha * (outcome[i] - res[i])
            delta_w1 += alpha * operator[i][0] * (outcome[i] - res[i])
            delta_w2 += alpha * operator[i][1] * (outcome[i] - res[i])
        w0 += delta_w0
        w1 += delta_w1
        w2 += delta_w2
        if res == outcome:
            break
        if epochs >= 10000:
            return epochs
        epochs += 1
    return epochs


# to study the results, run the program 30 times and record the average
def test_runner(operator_and, alphas, operator_xor):
    operators = [(0, 0), (0, 1), (1, 0), (1, 1)]
    results_and = [0, 0, 0, 1]
    results_or = [0, 1, 1, 1]
    results_xor = [0, 1, 1, 0]

    colors = ['green', 'red']
    c = 0

    for alpha in alphas:
        times = 0
        epochs = []
        run_times = []
        while times < 30:
            random.seed(times)
            start = timeit.default_timer()
            if operator_and:
                epochs.append(executor(operators, results_and, alpha))
            else:
                if operator_xor:
                    print("More than" + str(executor(operators, results_xor, alpha))
                          + " - XOR operator is impossible to solve")
                    break
                else:
                    epochs.append(executor(operators, results_or, alpha))
            end = timeit.default_timer()
            run_times.append(end - start)
            times += 1
        plot_boxplot(run_times, operator_and, alpha)
        plot_chart(epochs, operator_and, alpha, colors[c])
        c += 1


def plot_chart(epochs, operator_and, alpha, color):
    plt.suptitle('Epochs for operator ' + ('AND' if operator_and else 'OR'))
    plt.title(' Alfa=' + str(alpha))
    plt.ylabel('Epochs')
    plt.xlabel('Experiments')
    plt.plot([a for a in range(30)], epochs, c=color, alpha=1, marker='.', )
    plt.show()


def plot_boxplot(times, operator_and, alpha):
    plt.suptitle('Run times for operator ' + ('AND' if operator_and else 'OR'))
    plt.title(' Alfa=' + str(alpha))
    plt.ylabel('Run times')
    plt.xlabel('μ={:.6f} σ={:.6f}'.format((sum(times) / len(times)), st.pstdev(times)))
    plt.boxplot(times)
    plt.show()


if __name__ == '__main__':
    test_runner(operator_and=False, alphas=[0.1, 0.9], operator_xor=False)
