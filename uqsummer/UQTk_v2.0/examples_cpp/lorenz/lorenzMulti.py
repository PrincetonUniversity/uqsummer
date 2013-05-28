#!/usr/bin/env python


import os
import shutil
import sys
import numpy as np
import math
import random as rnd
from scipy.stats.mstats import mquantiles

import fileinput

## The main program
#
def main(args):
    # Load the parameter samples
    params=np.loadtxt("param.dat")
   
    if len(params.shape)==1:
        params=np.array([params])


    nruns=params.shape[0]
    ndim=params.shape[1]
    print nruns, ndim

    # Species id to analyze (1=u, 2=v, 3=w)
    # Currently set to u
    spid=1

    allsol=[]
    ave=[]
    period=[]
    for ip in range(nruns):

        # Create the xml files
        shutil.copyfile('surf_rxn.in.xml.templ','surf_rxn.in.xml')
        for idim in range(ndim,0,-1):
            for line in fileinput.input("surf_rxn.in.xml", inplace = 1):
                print line.replace('PAR_'+str(idim), str(params[ip,idim-1])),

        print("======================================================================================================================")
        print("Running the ODE solver for parameter %d/%d" % (ip+1,nruns))
        os.system('./SurfRxnDet.x')

        # Store the solution file
        shutil.copyfile('solution.dat','solution_'+str(ip)+'.dat')
        cursol=np.loadtxt("solution.dat")
        allsol.append(cursol)

        # Get the second half of the time series 
        tail=cursol.shape[0]/2

        # Compute the average of the given species
        ave.append(np.average(cursol[-tail:,spid]))

        # Estimate the period using Fourier spectrum of the given species
        # Need to have enough number of oscillations in the time series
        arr=np.fft.rfft(cursol[-tail:,spid])
        period.append(tail/(abs(arr[1:]).argmax()))

    print "Average: ", np.array(ave)
    print "Period: ", np.array(period)

## Execute main if this file is run as a script
#
if __name__ == "__main__":
    main(sys.argv[1:])


