import numpy as np
from consts import CARDS, COUNTS
from pocker import Player, Game
from utils import activation, derivative_activation, rand


class Net():

    def __init__(self):
        input_layer = (
            CARDS +
            ["check", "c_check"] +
            ["reraise_%s" % c for c in COUNTS] +
            ["c_reraise_%s" % c for c in COUNTS] +
            ["bed_%s" % c for c in COUNTS] +
            ["c_bed_%s" % c for c in COUNTS]
        )

        self.attr_to_key = dict((a, idx) for idx, a in enumerate(input_layer))
        self.size_level_1 = 25
        self.output_level = [
            ("check", ),
            ("pass", ),
        ] + [("bed", c) for c in COUNTS] + [("reraise", c) for c in COUNTS]
        self.size_output_level = len(self.output_level)

        self.W = rand(len(input_layer), self.size_level_1)
        self.W2 = rand(self.size_level_1, self.size_output_level)

        self.summator_l1 = np.zeros(self.size_level_1)
        self.summator_output_level = np.zeros(self.size_output_level)

    def get_decigion(self, data_set):
        self.summator_l1 = np.zeros(self.size_level_1)
        for d in data_set:
            for n1_idx, w in enumerate(self.W[self.attr_to_key[d]]):
                self.summator_l1[n1_idx] += w * 1
        self.summator_l1 = [activation(x) for x in self.summator_l1]

        self.summator_output_level = np.zeros(self.size_output_level)
        for idx_l1, d in enumerate(self.summator_l1):
            for n2_idx, w in enumerate(self.W2[idx_l1]):
                self.summator_output_level[n2_idx] += w * 1

        self.summator_output_level = [activation(x) for x in self.summator_output_level]

        return sorted(
            zip(self.output_level, self.summator_output_level),
            key=lambda x: x[1],
            reverse=True,
        )

    def teach(self, data_set, factor):
        decigion = self.get_decigion(data_set)[0]
        yk = decigion[1]
        a = abs(factor / 10)
        diff = 0.05
        if factor > 0:
            tk = min(yk + diff, 1)
        elif factor < 0:
            tk = max(yk - diff, 0)

        sig_k = (tk - yk) * derivative_activation(yk)

        for out_idx, out in enumerate(self.output_level):
            if out != decigion[0]:
                continue

            for z_idx, w2s in enumerate(self.W2):
                asd = a * sig_k * self.summator_output_level[out_idx]



        return


if __name__ == '__main__':

    nnet = Net()

    pl1 = Player('Boris', nnet)
    pl2 = Player('Ivan', nnet)

    game = Game(pl1, pl2)
    counter = 0
    while pl1.balance > 0 and pl2.balance > 0:
        counter += 1

        pl1_balance_before = pl1.balance
        pl2_balance_before = pl2.balance

        game.next_turn()
        assert pl1.balance + pl2.balance == 200

        nnet.teach(pl1.steps, pl1.balance - pl1_balance_before)
        nnet.teach(pl2.steps, pl2.balance - pl2_balance_before)

        pl1.steps = []
        pl2.steps = []

    print(counter)
