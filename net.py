import math
import numpy as np
from const import CARDS


def sigmoid(x): return 1 / (1 + math.exp(-x))


attr = CARDS
attr_to_key = dict((a, idx) for idx, a in enumerate(attr))

count_attr = len(attr)
size_level_1 = 5
size_output_level = 3


W = np.random.rand(count_attr, size_level_1)
W2 = np.random.rand(size_level_1, size_output_level)


def calculate_level(data_set):
    pass


def teach(data_set):
    summator_l1 = np.zeros(size_level_1)
    for d in data_set:
        for n1_idx, w in enumerate(W[attr_to_key[d]]):
            summator_l1[n1_idx] += w * 1
    summator_l1 = [sigmoid(x) for x in summator_l1]

    summator_output_level = np.zeros(size_output_level)
    for idx_l1, d in enumerate(summator_l1):
        for n2_idx, w in enumerate(W2[idx_l1]):
            summator_output_level[n2_idx] += w * 1

    summator_output_level = [sigmoid(x) for x in summator_output_level]

    return summator_output_level


if __name__ == '__main__':
    data_set = ["K"]
    print(teach(data_set))
