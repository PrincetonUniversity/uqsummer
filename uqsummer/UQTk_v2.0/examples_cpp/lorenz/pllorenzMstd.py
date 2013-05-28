#!/usr/bin/env python

import os
import sys 
import numpy as np
from   scipy import stats
import matplotlib
import matplotlib.pylab as plt

import plot_utils as ut

method=sys.argv[1]

# Read data file into numpy array
odeData = ut.ReadDataFile("solution_"+method+".dat")

# Define stride to reduce data
stride = 10
# extract x coordinates
xCoords = odeData[::stride,0]

# font and linewidth parameters

# lw is line width
# fs is font size
lw,fs = ut.SetPlotParams()
elw = lw/2 # error bar line width

# create figure and axis
fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])

# set axis limits
# ax.set_xlim([0,1000])
# ax.set_ylim([0,1])

# plot mean u, v, w vs. x and add error bars: +/- one std dev.
pleg = []
pleg.append(plt.errorbar(xCoords,odeData[::stride,1],odeData[::stride,2],linewidth=lw,elinewidth=elw)) # u, std dev u
# pleg.append(plt.errorbar(xCoords,odeData[::stride,3],odeData[::stride,4],linewidth=lw,elinewidth=elw)) # v, std dev v
# pleg.append(plt.errorbar(xCoords,odeData[::stride,5],odeData[::stride,6],linewidth=lw,elinewidth=elw)) # w, std dev w

plt.xlabel("Time [-]",fontsize=fs)
plt.ylabel("state variables",fontsize=fs)

# leg = plt.legend( (pleg[0][0], pleg[1][0], pleg[2][0]),
#                   (r"$u$"    , r"$v$"    , r"$w$"    ), loc='upper right', ncol=3)
leg = plt.legend( (pleg[0][0],),
                  (r"$u$"    ,), loc='upper right', ncol=3)

plt.title("Method " + method,fontsize=fs)

plt.savefig("prob2_lorenz_"+method+"_mstd.pdf")
                  


