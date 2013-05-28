#!/usr/bin/env python


import os
import shutil
import sys
import numpy as np
import math
import random as rnd
from scipy import stats, mgrid, c_, reshape, random, rot90
import matplotlib.pyplot as plt
from utils import get_npc

import fileinput

from pylab import *

rc('legend',loc='upper left', fontsize=22)
rc('lines', linewidth=4, color='r')
rc('axes',linewidth=3,grid=True,labelsize=22)
rc('xtick',labelsize=20)
rc('ytick',labelsize=20)

# define uqtkbin
if os.environ.get("UQTK_SRC") is None:
    print "Error: Need to set path to uqtk src as environment variable UQTK_SRC -> Abort"
    quit()

uqtkbin=os.environ["UQTK_SRC"]+"/src_cpp/bin"
pcerv=uqtkbin+"/pce_rv"


species=sys.argv[1] # u v w
qoi=sys.argv[2] #ave tf
pctype=sys.argv[3]
ord=int(sys.argv[4])
methlist=sys.argv[5:]

nsam=100000


if (species=='u'):
    spid=1
elif (species=='v'):
    spid=2
elif (species=='w'):
    spid=3



fig = plt.figure(figsize=(8,6))
ax=fig.add_axes([0.12,0.10,0.83,0.85])


for method in methlist:
    sol=np.loadtxt("solution_"+method+"_modes.dat")


    # Get the second half of the time series 
    tail=sol.shape[0]/2

    # Compute the average of the given species
    if (qoi=='ave'):
        ave=np.average(sol[-tail:,1:],axis=0)
        ncol=ave.shape[0]
        npc=ncol/3
        np.savetxt("pccf.dat",ave[npc*(spid-1):npc*spid])
    elif (qoi=='tf'):
        sp_tf=np.array(sol[-1,1:])
        ncol=sp_tf.shape[0]
        npc=ncol/3
        np.savetxt("pccf.dat",sp_tf[npc*(spid-1):npc*spid])

    # Find (in a very unpleasant way) the stochastic dimension
    for dim in range(1,7):
        npcc=get_npc(dim,ord)
        if (npc==npcc):
            break
    
        
    pcerv=uqtkbin+"/pce_rv"
    os.system(pcerv+" -w'PC' -f'pccf.dat' -x" + pctype + " -d1 -n" + str(nsam) +" -p"+str(dim)+" -q"+str(ord))

    spls=np.genfromtxt("rvar.dat")

    xlin=np.linspace(spls.min(),spls.max(),100) ;
    kernlin=stats.kde.gaussian_kde(spls);
    pdflin1=kernlin(xlin);

    plt.plot(xlin,pdflin1,linewidth=2,label=method)


ax.set_xlabel("PC representation",fontsize=24)
ax.set_ylabel("PDF",fontsize=24)
plt.title("Species: "+species+", QoI: "+qoi,fontsize=24)
plt.legend(loc="upper right")
plt.savefig("prob2_"+species+"_"+qoi+"_PCEdens.pdf")





