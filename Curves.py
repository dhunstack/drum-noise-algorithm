import numpy as np

def exp(x, A, B):
    return np.exp(-A*x) * (1 - np.exp(-B * x))