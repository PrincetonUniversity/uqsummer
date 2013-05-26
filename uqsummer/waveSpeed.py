import matplotlib.pyplot as plt
import numpy as np
f = plt.figure()
a = f.gca()

f2 = plt.figure()
a2 = []
X = np.arange(0, 2*np.pi, 0.01)
times = np.arange(0, 4, 0.01)
ntries = 5
for ax in range(ntries):
    a2.append(f2.add_subplot(1, ntries, ax+1))
    Z = np.random.uniform(-1, 1)
    norms = []
    U = X.copy()
    history = np.zeros((len(times), len(X)))
    print history.shape
    for i, t in enumerate(times):
        for j in range(len(X)):
            U[j] = np.cos(X[j] - Z * t)
            history[i,j] = U[j]
        norms.append(np.linalg.norm(U))
    a.plot(times, norms, label="Z=%.2f" % Z)
    a2[-1].imshow(history)
a.legend(loc="best")
a.set_xlabel("time")
a.set_ylabel("2-norm norm of solution")
plt.show()
