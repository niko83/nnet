import math
import numpy as np
#  https://habrahabr.ru/post/198268/


def rand(x, y):
    W = np.random.rand(x, y)
    return [[j - 0.5 for j in I] for I in W]


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
    return derivative_sigmoid(x)
