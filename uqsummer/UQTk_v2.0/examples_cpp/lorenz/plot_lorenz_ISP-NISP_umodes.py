#!/usr/bin/env python

import os
import sys 
import numpy as np
from   scipy import stats
import matplotlib
import matplotlib.pylab as plt

import plot_utils as ut

# Read data file into numpy array
odeDataISP = ut.ReadDataFile("solution_ISP.dat")
odeDataNISP = ut.ReadDataFile("solution_NISP.dat")

# Define stride to reduce data
stride = 10

# extract x coordinates
xCoordsISP = odeDataISP[::stride,0]
xCoordsNISP = odeDataNISP[::stride,0]

# font and linewidth parameters

# lw is line width
# fs is font size
lw,fs = ut.SetPlotParams()

# create figure and axis
fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])

# set axis limits
ax.set_xlim([0,1000])
ax.set_ylim([-0.01,0.005])

# plot 2 highest order modes for u with NISP and ISP
ord = 5
pleg = []
for i in range(ord-1,ord+1):
    pleg.append(plt.plot(xCoordsISP,odeDataISP[::stride,i+1],linewidth=lw)) # u_i
    pleg.append(plt.plot(xCoordsNISP,odeDataNISP[::stride,i+1],linewidth=lw)) # u_i

plt.xlabel("Time [-]",fontsize=fs)
plt.ylabel("$u_i$ [-]",fontsize=fs)

leg = plt.legend( (pleg[0][0], pleg[1][0], pleg[2][0], pleg[3][0]),
                  (r"$u_{4,ISP}$"  , r"$u_{4,NISP}$"  , r"$u_{5,ISP}$"  , r"$u_{5,NISP}$" ), loc='lower left', ncol=2)

plt.savefig("surf_rxn_ISP-NISP_umodes.pdf")
                  


