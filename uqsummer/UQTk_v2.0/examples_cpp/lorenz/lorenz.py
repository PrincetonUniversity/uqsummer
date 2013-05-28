from tomDefaults import *
import tomIntegrate as ti
import matplotlib.pyplot as plt
import numpy as np

def diff(X, t=0):
    a = 10.0
    b = 4.0
    c = 2.66
    u = X[0]
    v = X[1]
    w = X[2]
    dudt = a * (v - u);
    dvdt = u * (b - w) - v;
    dwdt = u * v - c * w;
    return np.array([dudt, dvdt, dwdt])

def showIt():
    initial = np.array([1, 1, 1])
    X, t = ti.doint(initial, diff, tmax=1)
    print X.shape
    for i in range(3):
        a.plot(t, X[:,i])
    plt.show()
    
    
if __name__=="__main__":
    showIt()