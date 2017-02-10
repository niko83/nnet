import math
import numpy as np
from consts import CARDS



 #  https://habrahabr.ru/post/198268/

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def derivative_sigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))


def bip_sigmoid(x):
    return 1 / (1 + math.exp(-x)) - 1


def derivative_bip_sigmoid(x):
    return 0.5 * (1 + bip_sigmoid(x)) * (1 - bip_sigmoid(x))


def activation(x):
    return sigmoid(x)


def derivative_activation(x):
    derivative_sigmoid(x)




def rand(x, y):
    W = np.random.rand(x, y)
    return [[j - 0.5 for j in I] for I in W]


attr = CARDS
attr_to_key = dict((a, idx) for idx, a in enumerate(attr))

count_attr = len(attr)
size_level_1 = 5
size_output_level = 3

W = rand(count_attr, size_level_1)
W2 = rand(size_level_1, size_output_level)


def calculate_level(data_set):
    pass


def teach(data_set):
    summator_l1 = np.zeros(size_level_1)
    for d in data_set:
        for n1_idx, w in enumerate(W[attr_to_key[d]]):
            summator_l1[n1_idx] += w * 1
    summator_l1 = [activation(x) for x in summator_l1]

    summator_output_level = np.zeros(size_output_level)
    for idx_l1, d in enumerate(summator_l1):
        for n2_idx, w in enumerate(W2[idx_l1]):
            summator_output_level[n2_idx] += w * 1

    summator_output_level = [activation(x) for x in summator_output_level]

    return summator_output_level


if __name__ == '__main__':
    data_set = ["K"]
    print(teach(data_set))
