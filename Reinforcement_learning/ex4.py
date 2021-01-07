import enum
import random
import numpy as np
import matplotlib.pyplot as plt
import timeit
import statistics as st


class Node:
    def __init__(self, next_state=None, next_action=None, current_utility=None, next_index=None):
        self.next_state = next_state
        self.next_action = next_action
        self.current_utility = current_utility
        self.next_index = next_index


class Actions(enum.Enum):
    left = 'left'
    right = 'right'
    up = 'up'
    down = 'down'


def print_2d_array(v):
    np.set_printoptions(precision=2, suppress=True)
    new_v = [round(i, 2) for i in v]
    print(np.reshape(new_v, (10, 10)))


def heuristic(s):
    if s == 100:
        return 100
    return 0


def ex4():
    state_size = 100

    maze = [(i+1) for i in range(state_size)]
    v = [0 for _ in range(state_size)]

    alpha = 0.3
    discount = 0.95

    runner(maze, alpha, discount, v)


def next_moves(state):
    moves = [Node((state + 1), Actions.left.value, None, None),
             Node((state - 1), Actions.right.value, None, None),
             Node((state - 10), Actions.down.value, None, None),
             Node((state + 10), Actions.up.value, None, None)]
    return moves


def is_valid_actions(state, next_state: Node):
    if state % 10 != 0 and next_state.next_action == Actions.left.value:
        return True
    if state % 10 != 1 and next_state.next_action == Actions.right.value:
        return True
    if state - 10 > 0 and next_state.next_action == Actions.down.value:
        return True
    if state + 10 < 101 and next_state.next_action == Actions.up.value:
        return True
    return False


def random_move(state):
    moves = next_moves(state)
    return random.choice(moves)


def state_transaction(state):
    return random_move(state)


def executor(maze, v, alpha, discount, times):
    start = timeit.default_timer()
    rewards = 0
    current_state = maze[0]
    i = 0
    path = []

    while i < times:
        next_state = state_transaction(current_state)
        path.append(next_state.next_action)

        if is_valid_actions(current_state, next_state):
            v[current_state - 1] = \
                (1 - alpha) * v[current_state - 1] + alpha * \
                (heuristic(current_state) + discount * v[next_state.next_state - 1])

            # if it reached the reward position increment rewards
            rewards += heuristic(next_state.next_state)
            # update current state
            if current_state == 100:
                current_state = maze[0]
            else:
                current_state = maze[next_state.next_state - 1]
        else:
            next_state.next_state = current_state
            v[current_state - 1] = \
                round((1 - alpha) * v[current_state - 1] + alpha *
                      (heuristic(next_state.next_state) + discount * v[next_state.next_state - 1]), 2)

        i += 1
    end = timeit.default_timer()

    times_on_reward = rewards / 100
    reward_per_state = rewards / times

    # print(len(path), "actions: ", path)
    print("experiment occurred", times, "times and got", rewards, "rewards. Times reaching the goal:",
          times_on_reward, "with an average of:", reward_per_state, "reward per state")

    if times == 20000:
        print_2d_array(v)
        heat_map(v, alpha, discount)

    return end - start, reward_per_state


def runner(maze, alpha, discount, v):
    trials = 0
    results = []
    executor(maze, v, alpha, discount, 20000)
    while trials < 30:
        random.seed(trials)
        results.append(executor(maze, v, alpha, discount, 1000)[1])
        trials += 1
    # plot_chart(results)
    plot_boxplot(results, alpha, discount)


def plot_boxplot(results, alpha, discount):
    plt.suptitle('Run times during experiments')
    plt.title('Alfa=' + str(alpha) + ' Discount=' + str(discount))
    print("In 20.000 steps the run time average is:", (sum(results) / len(results)))
    plt.ylabel('Run times (s)')
    plt.xlabel('μ={:.4f} σ={:.4f}'.format((sum(results) / len(results)), st.pstdev(results)))
    plt.boxplot(results)
    plt.show()


def heat_map(v, alpha, discount):
    plt.suptitle('Run times during experiments')
    plt.title('Alfa=' + str(alpha) + ' Discount=' + str(discount))
    plt.imshow(np.reshape(v, (10, 10)), cmap='hot', interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    ex4()
