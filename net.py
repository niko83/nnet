import numpy as np
from consts import CARDS, COUNTS, BALANCE, DIFF
from pprint import pprint
from pocker import Player, Game
from copy import deepcopy
from utils import activation, derivative_activation, rand
from termcolor import colored
import sys


class Net():

    def __init__(self):
        self.input_layer = (
            CARDS +
            ["check", "c_check"] +
            ["reraise_%s" % c for c in COUNTS] +
            ["c_reraise_%s" % c for c in COUNTS] +
            ["bed_%s" % c for c in COUNTS] +
            ["c_bed_%s" % c for c in COUNTS]
        )

        self.attr_to_key = dict((a, idx) for idx, a in enumerate(self.input_layer))
        self.output_level = [
            ("check", '_'),
            ("pass", '_'),
        ] + [("bed", c) for c in COUNTS] + [("reraise", c) for c in COUNTS]
        self.size_output_level = len(self.output_level)

        self.size_level_1 = self.size_output_level

        self.W = rand(len(self.input_layer), self.size_level_1)
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
            for output_idx, w in enumerate(self.W2[idx_l1]):
                self.summator_output_level[output_idx] += w * d

        self.summator_output_level = [activation(x) for x in self.summator_output_level]

        return sorted(
            zip(self.output_level, self.summator_output_level),
            key=lambda x: x[1],
            reverse=True,
        )

    def print_tree(self):
        o = []
        o.append("")
        o.append("W:")

        for input_idx, w in enumerate(self.W):
            tpl = "{:12s}:" + "{:8.4f} " * len(w)
            o.append(tpl.format(self.input_layer[input_idx], *w))

        o.append("")
        o.append("W2:")
        o.append(
            ("{:3s}:" + "{:>16s} "*len(self.output_level)).format(".", *[str(i) for i in self.output_level])
        )
        for z_idx, w in enumerate(self.W2):
            tpl = "{:3}:" + "{:>16.4f} " * len(w)
            o.append(tpl.format(z_idx, *w))

        o.append("")
        o.append("Decigions:")

        for c in CARDS:
            for decigion in self.get_decigion([c]):
                if decigion[0][0] in ('bed', 'check'):
                    break
            o.append("%3s %15s %10.5f" % (c, decigion[0], decigion[1]))
            o.append(("             Sum1: " + "{:8.4f}"*len(self.summator_l1)).format(*self.summator_l1))

            o.append(("       Sum output: " + "{:>16s}"*len(self.output_level)).format(*[str(i) for i in self.output_level]))
            o.append(("                   " + "{:>16.4f}"*len(self.summator_output_level)).format(*self.summator_output_level))

        return '\n'.join(o)

    def print_tree_diff(self, before_W2, before_decigions):
        o = []
        o.append("--------------------------------")
        o.append(colored("W2:", 'green'))


        o.append(
            ("{:12s}:" + "{:>25s}"*len(self.output_level)).format(
                "", *[colored('%s_%s' % (i[0], i[1]),'white') for i in self.output_level]
            ))

        for input_idx, W in enumerate(self.W2):
            tpl = "{:12s}:" + "{:>25s} " * len(W)
            w = []
            for w_idx, w_data in enumerate(W):
                if w_data > before_W2[input_idx][w_idx]:
                    clr = 'green'
                elif w_data < before_W2[input_idx][w_idx]:
                    clr = 'red'
                else:
                    clr = 'yellow'
                w.append(colored('{:>.4f}'.format(w_data-before_W2[input_idx][w_idx]), clr))

            o.append(tpl.format(str(input_idx), *w))

        return '\n'.join(o)


    def teach(self, data_set, decigion, factor):
        for d in self.get_decigion(data_set):
            if d[0] == decigion:
                decigion = d
                break
        else:
            raise Exception()

        yk = decigion[1]
        a = abs(factor / 10)
        if factor > 0:
            tk = min(yk + DIFF, 1)
        elif factor < 0:
            tk = max(yk - DIFF, 0)
        else:
            return

        sig_k = (tk - yk) * derivative_activation(yk)

        for out_idx, out in enumerate(self.output_level):
            if out != decigion[0]:
                continue

            for w2s in self.W2:
                w2s[out_idx] += a * sig_k

        for z_idx, sum1 in enumerate(self.summator_l1):
            sig_k = DIFF * derivative_activation(sum1)
            for ws in self.W:
                if factor > 0:
                    ws[z_idx] += a * sig_k
                elif factor < 0:
                    ws[z_idx] -= a * sig_k


class NetRandom(Net):
    def get_decigion(self, steps):

        return sorted(
            zip(self.output_level, self.summator_output_level),
            key=lambda x: x[1],
            reverse=True,
        )


if __name__ == '__main__':

    nnet = Net()
    print(nnet.print_tree())

    before_W2 = deepcopy(nnet.W)
    before_decigions = []
    for c in CARDS:
        before_decigions.append(nnet.get_decigion([c]))

    for i in range(30):
        nnet.teach(['A'], ("bed", 10), 30)
        nnet.teach(['K'], ("bed", 5), 30)
        #  nnet.teach(['Q'], ("pass", '_'), 30)
        #  nnet.teach(['J'], ("pass", '_'), 30)

    print(nnet.print_tree_diff(before_W2, before_decigions))
    print(nnet.print_tree())

    sys.exit(1)
    nnet2 = Net()

    pl1 = Player('Boris', nnet)
    pl2 = Player('Ivan', nnet2)

    game = Game(pl1, pl2)

    counter = 0
    while pl1.balance > 0 and pl2.balance > 0:
        counter += 1

        pl1_balance_before = pl1.balance
        pl2_balance_before = pl2.balance

        before_W2 = deepcopy(nnet.W)
        before_decigions = []
        for c in CARDS:
            before_decigions.append(nnet.get_decigion([c]))

        game.next_turn()
        assert pl1.balance + pl2.balance == BALANCE * 2
        if counter % 1000 == 0:
            print(pl1.balance, pl2.balance)


        nnet.teach(pl1.steps, pl1.balance - pl1_balance_before)
        print('=======================')
        print(pl1.steps)
        print(pl1.balance - pl1_balance_before)
        print(nnet.print_tree_diff(before_W2, before_decigions))
        nnet2.teach(pl2.steps, pl2.balance - pl2_balance_before)
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT


        pl1.steps = []
        pl2.steps = []

    print(nnet.print_tree())

    print(counter)
