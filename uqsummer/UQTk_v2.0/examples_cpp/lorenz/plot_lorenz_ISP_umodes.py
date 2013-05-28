#!/usr/bin/env python

import os
import sys 
import numpy as np
from   scipy import stats
import matplotlib
import matplotlib.pylab as plt

import plot_utils as ut

# Read data file into numpy array
odeData = ut.ReadDataFile("solutionISP.dat")

# Define stride to reduce data
stride = 1000

# extract x coordinates
xCoords = odeData[::stride,0]

# font and linewidth parameters

# lw is line width
# fs is font size
lw,fs = ut.SetPlotParams()

# create figure and axis
fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])

# set axis limits
ax.set_xlim([0,1000])
ax.set_ylim([-0.1,0.55])

# plot 6 modes of u
ord = 5
pleg = []
for i in range(ord+1):
    pleg.append(plt.plot(xCoords,odeData[::stride,i+1],linewidth=lw)) # u_i

plt.xlabel("Time [-]",fontsize=fs)
plt.ylabel("$u_i$ [-]",fontsize=fs)

leg = plt.legend( (pleg[0][0], pleg[1][0], pleg[2][0], pleg[3][0], pleg[4][0], pleg[5][0]),
                  (r"$u_0$"  , r"$u_1$"  , r"$u_2$"  , r"$u_3$"  , r"$u_4$", r"$u_5$"    ), loc='upper center', ncol=3)

plt.savefig("surf_rxn_ISP_umodes.pdf")
                  
