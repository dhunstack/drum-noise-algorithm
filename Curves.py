import numpy as np

def exp(x, A, B):
    return np.exp(-A*x) * (1 - np.exp(-B * x))

def exprel(x, A, B, C):
    relT = np.argmax(x >= C)
        
    r1 =  np.exp(-A * x[0:relT]) * (1 - np.exp(-B * x[0:relT]))
    r2 = np.exp(-A * C) * (1 - np.exp(-B * C)) * np.exp(-(x[relT:] - C))

    return np.append(r1, r2)