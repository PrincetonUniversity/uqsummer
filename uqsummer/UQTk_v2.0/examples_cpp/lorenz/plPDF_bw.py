#!/usr/bin/env python


import os
import shutil
import sys
import numpy as np
import math
import random as rnd
from scipy.stats.mstats import mquantiles

import fileinput
from prob3_utils import plotKdeBin


# define uqtkbin
if os.environ.get("UQTK_SRC") is None:
    print "Error: Need to set path to uqtk src as environment variable UQTK_SRC -> Abort"
    quit()

uqtkbin=os.environ["UQTK_SRC"]+"/src_cpp/bin"
pcerv=uqtkbin+"/pce_rv"


sol=np.loadtxt("solution_NISP_modes.dat")
species=sys.argv[1] # u v w
qoi=sys.argv[2] #ave tf
dim=1
ord=3
nsam=10000
pctype='HG'

if (species=='u'):
    spid=1
elif (species=='v'):
    spid=2
elif (species=='w'):
    spid=3
 


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


pcerv=uqtkbin+"/pce_rv"
os.system(pcerv+" -w'PC' -f'pccf.dat' -x" + pctype + " -d1 -n" + str(nsam) +" -p"+str(dim)+" -q"+str(ord))
plotKdeBin("rvar.dat",species+"_"+qoi+"_PCEdens.eps",npdf=100)
