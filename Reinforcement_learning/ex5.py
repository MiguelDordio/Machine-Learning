import random
import numpy as np
import matplotlib.pyplot as plt
import timeit
import statistics as st


def print_2d_array(q_matrix):
    np.set_printoptions(precision=2, suppress=True)
    print(np.reshape(q_matrix, (len(q_matrix), len(q_matrix[0]))))


def heuristic(s):
    if s == 100:
        return 100
    return 0


def ex5(evaluate_time, learning_mode):
    action_size = 4
    state_size = 100

    # A=0.3 D=0.95 e A=0.1 D=0.95 A=0.3 D=0.99
    alpha = 0.3
    discount = 0.95

    trials = 0
    results = []
    measures = [0, 100, 200, 500, 600, 700, 800, 900, 1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 19999]
    while trials < 30:
        random.seed(trials)
        q_matrix = [[round(random.uniform(0.01, 0.99), 2) for _ in range(action_size)] for _ in range(state_size)]
        results.append(trainer(q_matrix, alpha, discount, 20000, learning_mode, evaluate_time))
        if trials == 29:
            heat_map(q_matrix, learning_mode, alpha, discount)
        trials += 1

    plt.suptitle(('Run times during experiments - ' if evaluate_time else 'Average reward per state evaluations - ')
                 + ('Guided Training' if learning_mode else 'Random Training'))
    plt.title('Alfa=' + str(alpha) + ' Discount=' + str(discount))
    if evaluate_time:
        print("In 20.000 steps the run time average is:", (sum(results) / len(results)))
        plt.ylabel('Run times (s)')
        plt.xlabel('μ={:.4f} σ={:.4f}'.format((sum(results) / len(results)), st.pstdev(results)))
        plot_boxplot(results)
    else:
        plt.ylabel('Average rewards per step')
        plt.xlabel('Measure points')
        avg_results = []
        for i in range(len(measures)):
            sum_measure = 0
            # lis is the list of avg results of each 1 of the 30 experiments
            for lis in results:
                sum_measure += lis[i]
            avg_results.append(sum_measure / 30)
        print(avg_results)
        plot_chart(avg_results, measures)


def next_moves(state):
    return [((state + 1), 'left'), ((state - 1), 'right'), ((state - 10), 'down'), ((state + 10), 'up')]


def is_valid_actions(state, direction):
    if state % 10 != 0 and direction == 'left':
        return True
    if state % 10 != 1 and direction == 'right':
        return True
    if state - 10 > 0 and direction == 'down':
        return True
    if state + 10 < 101 and direction == 'up':
        return True
    return False


def best_move(state, q_matrix):
    moves = next_moves(state)
    best_move_index = q_matrix[state - 1].index(max(q_matrix[state - 1]))
    return moves[best_move_index], best_move_index


def random_move(state):
    moves = next_moves(state)
    rand_move = random.choice(moves)
    return rand_move, moves.index(rand_move)


def state_transaction(state, q_matrix, learning_mode):
    if learning_mode:
        next_state, next_index = best_move(state, q_matrix)
    else:
        next_state, next_index = random_move(state)

    valid_move = is_valid_actions(state, next_state[1])
    if valid_move:
        return next_state[0], next_index, valid_move, next_state[1]
    else:
        return state, next_index, valid_move, None


def trainer(q_matrix, alpha, discount, times, learning_mode, evaluate_time):
    start = timeit.default_timer()
    current_state = 1
    path = []
    avg_reps = []
    rewards = 0
    i = 0
    while i < times:
        # get next state
        next_state, next_index, valid_move, direction = state_transaction(current_state, q_matrix, learning_mode)

        # add next state to path
        path.append(next_state)

        # update Q matrix
        q_matrix[current_state - 1][next_index] = \
            (1 - alpha) * q_matrix[current_state - 1][next_index] + alpha * \
            (heuristic(current_state) + discount * max(q_matrix[next_state - 1]))

        if valid_move:
            current_state = next_state

        # if current state is the goal go to the beginning
        if current_state == 100:
            # update Q matrix
            current_state_idx = q_matrix[current_state - 1].index(max(q_matrix[current_state - 1]))
            q_matrix[current_state - 1][current_state_idx] = \
                (1 - alpha) * q_matrix[current_state - 1][current_state_idx] + alpha * \
                (heuristic(current_state) + discount * max(q_matrix[current_state - 1]))
            rewards += heuristic(current_state)
            current_state = 1

        if not evaluate_time:
            if i == 0 or i == 100 or i == 200 or i == 500 or i == 600 or i == 700 or i == 800 \
                    or i == 900 or i == 1000 or i == 2500 or i == 5000 or i == 7500 or i == 10000 \
                    or i == 12500 or i == 15000 or i == 17500 or i == 19999:
                avg_reps.append(average_reward(q_matrix))

        i += 1
    # print_2d_array(q_matrix)

    end = timeit.default_timer()
    reward_per_state = rewards / times

    if learning_mode:
        print("Learning mode: Active | In 20000 steps: Total rewards:", rewards, " - Avg rewards per state:",
              reward_per_state)
    else:
        print("Learning mode: Inactive | In 20000 steps: Total rewards:", rewards, " - Avg rewards per state:",
              reward_per_state)

    return end - start if evaluate_time else avg_reps


def average_reward(q_matrix):
    trained_rewards = 0
    current_state = 1
    path = []
    j = 0
    n = 2
    while j < 1000:
        # get next best move
        next_state, next_index, valid_move, direction = state_transaction(current_state, q_matrix, True)
        path.append(next_state)

        # if the next move isn't valid
        while not valid_move:
            # get all possible moves
            moves = next_moves(current_state)
            # pick the n best move
            val_index = q_matrix[current_state - 1].index(sorted(q_matrix[current_state - 1])[-n])
            next_state = moves[val_index][0]
            valid_move = is_valid_actions(current_state, moves[val_index][1])
            n += 1

        # if its valid update current state
        if valid_move:
            current_state = next_state
            n = 2

        # if current state is the goal go to the beginning
        if current_state == 100:
            trained_rewards += heuristic(current_state)
            current_state = 1
        j += 1

    trained_rps = trained_rewards / 1000
    # print("average reward in 1000 steps: ", trained_rps)
    return trained_rps


def plot_boxplot(res):
    plt.boxplot(res)
    plt.show()


def plot_chart(average_rps, measures):
    plt.plot(measures, average_rps, c='blue')
    plt.show()


def heat_map(q_matrix, learning_mode, alpha, discount):
    plt.suptitle('Best path after training' + (' - Guided Training' if learning_mode else ' - Random Training'))
    plt.title('Alfa=' + str(alpha) + ' Discount=' + str(discount))
    best_q_matrix = [max(i) for i in q_matrix]
    plt.imshow(np.reshape(best_q_matrix, (10, 10)), cmap='hot', interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    ex5(evaluate_time=True, learning_mode=False)
