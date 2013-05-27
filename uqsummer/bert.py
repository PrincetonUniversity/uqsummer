import numpy as np
import matplotlib.pyplot as plt
import tomIntegrate as ti

def hermitePlotp24():
    p0 = lambda x: 1
    p1 = lambda x: x
    p2 = lambda x: x ** 2 - 1
    p3 = lambda x: x ** 3 - 3 * x
    
    X = np.arange(0, 2, 0.01)
    uf = lambda x: 0.5 * p0(x) + 0.2 * p1(x) + 0.1 * p2(x)
    
    Y = [uf(x) for x in X]
    
    plt.plot(X, Y)
    
    plt.show() 
    
def branched():
    def diff(u):
        a = 1.0
        return a * (u - 1) * (u + 10)
    for initial in [-1, 0, .5, 0.9, 0.99, 1.0001]:
        X, t = ti.doint([initial], diff, tmax=1)
        plt.plot(t, X)
    plt.show()

if __name__=="__main__":
#     hermitePlotp24()
    branched()