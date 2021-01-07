import random
import matplotlib.pyplot as plt
import timeit
import statistics as st


def heuristic(s):
    if s == 100:
        return 100
    return 0


def ex1_3(avg_rewards):
    trials = 0
    results = []
    while trials < 30:
        random.seed(trials)
        if avg_rewards:
            results.append(runner(1000, avg_rewards))
        else:
            results.append(runner(20000, avg_rewards))
        trials += 1

    if avg_rewards:
        plot_chart(results)
    else:
        plot_boxplot(results)


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


def state_transaction(state):
    next_state, next_index = random_move(state)
    valid_move = is_valid_actions(state, next_state[1])
    if valid_move:
        return next_state[0], next_index, valid_move, next_state[1]
    else:
        return state, next_index, valid_move, None


def runner(times, avg_rewards):
    start = timeit.default_timer()
    rewards = 0
    current_state = 1
    i = 0
    path = []

    while i < times:
        # get next state
        next_state, next_index, valid_move, direction = state_transaction(current_state)

        # add next state to path
        path.append(next_state)

        if valid_move:
            current_state = next_state

        # if current state is the goal go to the beginning
        if current_state == 100:
            rewards += heuristic(current_state)
            current_state = 1

        i += 1

    end = timeit.default_timer()
    times_on_reward = rewards / 100
    reward_per_state = rewards / times

    # print(len(path), "actions: ", path)
    print("experiment occurred", times, "times and got", rewards, "rewards. Times reaching the goal:",
          times_on_reward, "with an average of:", reward_per_state, "reward per state")

    return reward_per_state if avg_rewards else end - start


def plot_boxplot(results):
    plt.suptitle('Run times during experiments')
    plt.ylabel('Run times (s)')
    plt.xlabel('μ={:.4f} σ={:.4f}'.format((sum(results) / len(results)), st.pstdev(results)))
    plt.boxplot(results)
    plt.show()


def plot_chart(res):
    plt.suptitle('Average reward per state evaluations in 1000 steps')
    plt.ylabel('Average rewards per step')
    plt.xlabel('Experiments')
    plt.plot([i for i in range(30)], res, c='blue')
    plt.show()


if __name__ == '__main__':
    # if avg_rewards = True get the avg rewards else get the run times in 20k steps
    ex1_3(avg_rewards=True)
