#!/usr/bin/env python

import os
import sys 
import numpy as np
from   scipy import stats
import matplotlib
import matplotlib.pylab as plt

def ReadDataFile(dataFileName):
    """Read records in file with name dataFileName into
    a numpy matrix of floats"""

    # Open text file with all data
    dataFile = open(dataFileName,"r")

    # Convert all data lines into floats and put them in a list
    dataList = []
    for line in dataFile.readlines():
     records = line.split()
     numRecords = [float(s) for s in records]
     dataList.append(numRecords)

    dataFile.close()

    # Convert list to 2D numpy matrix object
    data = np.array(dataList)

    return data

def SetPlotParams():
    """ Set line widths and font sizes.
    Can be expanded down the road to take
    an argument like paper or slide. 
    Returns linewidth and fontsize. """

    linewidth = 2;
    fontsize = 16;

    return linewidth, fontsize
