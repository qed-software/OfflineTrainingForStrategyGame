import numpy as np


def initialize_actions():
    """

    """
    for i in range(9):
        State.actions_table.append((i, 2))
    State.actions_table.append((9, 0))
    State.actions_table.append((10, 0))
    State.actions_table.append((11, 0))


class State:
    actions_table = list()
    max_time = 40
    metadata = [
        [50, 20, 0, 5],  # 0  town hall
        [15, 0, 0, 5],  # 1  farm
        [30, 0, 0, 5],  # 2  barracks
        [20, 20, 0, 5],  # 3  archery range
        [20, 30, 0, 5],  # 4  stable
        [5, 0, 1, 0],  # 5  worker
        [5, 5, 1, 2],  # 6  pikeman
        [3, 7, 1, 3],  # 7  archer
        [15, 0, 2, 4],  # 8  cavarly
        [0, 0, 0, 5],  # 9  gold miners
        [0, 0, 0, 5]  # 10 lumberjacks
    ]

    names = {0: "Town Hall", 1: "Farm", 2: "Barracks", 3: "Archery Range", 4: "Stable", 5: "Worker", 6: "Pikeman",
             7: "Archer", 8: "Cavalry", 9: "Gold miner", 10: "Lumberman", 11: "Time"}

    def __init__(self):
        self.data = np.zeros([11, 3], dtype=int)
        self.food_used = 0
        self.time_step = 0
        self.gold = 15
        self.wood = 0
        self.data[0, 0] = 1
        self.data[1, 0] = 1

    def food(self):
        return 6 * self.data[1, 0] - self.food_used

    def apply_increase(self, row, column):
        if row < 11:
            self.data[row, column] += 1  # the main change
            self.data[self.metadata[row][3], 1] += 1  # makes something busy
            self.gold -= self.metadata[row][0]
            self.wood -= self.metadata[row][1]
            self.food_used += self.metadata[row][2]
        else:
            self.advance()

    def vectorize(self):
        v = list()
        v.append(self.gold)
        v.append(self.wood)
        v.append(self.food())
        for i in range(11):
            v.append(self.data[i, 0])
            v.append(self.data[i, 1])
            v.append(self.data[i, 2])
        return np.array(v)

    def advance(self):
        for index in range(9):
            if self.data[index, 2] > 0:
                self.data[index, 0] += self.data[index, 2]  # increases count
                self.data[self.metadata[index][3], 1] -= self.data[index, 2]  # makes something no longer busy
                self.data[index, 2] = 0
        self.gold += self.data[9, 0]
        self.wood += self.data[10, 0]
        self.time_step += 1

    def get_score(self):
        return min(self.data[6, 0], self.data[7, 0], self.data[8, 0])

    def gold_cost(self, index):
        return self.metadata[index][0]

    def wood_cost(self, index):
        return self.metadata[index][1]

    def food_cost(self, index):
        return self.metadata[index][2]

    def count(self, index):
        return self.data[index, 0]

    def busy(self, index):
        return self.data[index, 1]

    def queued(self, index):
        return self.data[index, 2]

    def is_legal(self, action_index):
        if action_index == 11:
            return True

        if self.gold >= self.gold_cost(action_index) and self.food() > self.food_cost(
                action_index) and self.wood >= self.wood_cost(action_index):
            req = self.metadata[action_index][3]
            return action_index < 5 or self.count(req) > self.busy(req)
        return False

    def apply_action(self, action_index):
        self.apply_increase(State.actions_table[0], State.actions_table[1])

    def apply_action_with_legal_fallback(self, action_index):
        if self.is_legal(action_index):
            self.apply_action(action_index)
        else:
            self.apply_action(11)

    def get_legal_actions(self):
        actions = list()
        for i in range(11):
            if self.is_legal(i):
                actions.append(State.actions_table[i])
        return actions

    def is_terminal(self):
        return self.time_step >= self.max_time

    def print(self):
        print("---------------------------------")
        print("Gold: {}, Wood: {}, Food: {}, Time: {}".format(self.gold, self.wood, self.food(), self.time_step))
        print("Busy/Count   Queued")
        for i in range(11):
            print("{}: {}/{} {}".format(self.names[i], self.busy(i), self.count(1),
                                        self.queued(i)))
