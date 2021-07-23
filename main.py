from numpy import genfromtxt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
from State import State, initialize_actions
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def run(model, max_time=40, print_output=False):
    State.max_time = max_time
    state = State()
    while not state.is_terminal():
        if print_output:
            state.print()
        X = np.zeros([1, 36], dtype=int)
        X[0] = state.vectorize()
        action_id = int(model.predict(X)[0])
        if print_output:
            print("---")
            print("Action id = {}".format(action_id))
            print("Gold:{}, Wood:{}, Food:{}".format(state.gold, state.wood, state.food()))
            input( )
        action = State.actions_table[action_id]
        if print_output:
            print("Action = advance {}".format(state.names[action_id]))
        state.apply_increase(action[0], action[1])
    score = state.get_score()
    print("Score {} for time={}: ".format(str(score), max_time))
    return score


if __name__ == "__main__":

    filename = "mcts_data.csv"
    data = genfromtxt(filename, delimiter=',')
    print("Loaded", filename)
    X, y = data[:, :-1], data[:, -1]
    print(X.shape)

    # train your model here.
    # simple example:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    clf = RandomForestClassifier(criterion='gini', n_estimators=60)
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    initialize_actions()
    repeats = 10
    max_game_time = 40
    total_score = 0
    for i in range(0, repeats):
        total_score += run(clf, max_game_time, False)

    average_score = total_score/repeats
    print("Average score: {}".format(average_score))
