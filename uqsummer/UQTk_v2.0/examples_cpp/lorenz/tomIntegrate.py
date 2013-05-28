from numpy import array, random, linspace, arange
import pylab as p
from scipy import integrate

###Integrating the ODE using scipy.integrate
def doint(initial, dxdt, tmin=0, tmax=800, nstep=1e5):
    def dxdtextra(X, t=0):
        return dxdt(X)
    t = linspace(tmin, tmax, nstep)
    X0 = array(initial)
    X, infodict = integrate.odeint(dxdtextra, X0, t, full_output=True)
    return X, t

def intor(initial, dxdt, **kwargs):
    '''
    Integrate forward from an initial condition.
    Initial condition is an n-tuple (or list) and dxdt is a rate function,
    like vdp
    Importannt kwargs are tmin, tmax, and nsteps
    '''
    return doint(initial, dxdt, **kwargs).T

def randr(a, b):
    '''1D uniform distribution between a and b. a < b'''
    if a > b:
        print "b > a, dumpass"
        return 4  # http://xkcd.com/221
    else:
        return random.rand() * (b - a) + a

def vdp(X, t=0):
    '''A Van der Pol oscillator system'''
    u = 4.0
    x = X[0]
    y = X[1]
    return array([
                    u * (y - F(x)),
                    -x / u
                ])

def lorenzGiver(r=15., s=10., b=2.66):
    return lambda X: lorenzkwarg(X, r=r, s=s, b=b)

def lorenzkwarg(X, r=15., s=10., b=2.66):
    x = X[0]
    y = X[1]
    z = X[2]
    F = lambda x: x ** 3 / 3 - x
    return array([
        s * (y - x),
        x * (r - z) - y,
        x * y - b * z
        ])

if __name__=="__main__":
    def F(x):
        return x ** 3 / 3 - x
    # Example 7.5.1

    numTrials = 10
    for i in range(numTrials):
        initial = (randr(-4, 4), randr(-4, 4))
        X, t = doint(initial, vdp)
        position = X[:,0]
        rate = X[:,1]
        p.plot(position, rate)
        p.scatter(initial[0], initial[1])
    fullrange = list(arange(-2.5, 2.5, .01))
    p.plot(fullrange, [F(x) for x in fullrange], 'k--')
    p.show()
