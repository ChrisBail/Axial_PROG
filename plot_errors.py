#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:41:09 2017

@author: baillard
"""

from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np
import math
import pylab
import re
from util import readxyz

### Parameters

input_file='dd.xyz'
input_file='nlloc_20m_GAU.xyz'

### Read

x_arr=readxyz(input_file)

rms=x_arr[-1]
x_err=x_arr[4]
y_err=x_arr[5]
z_err=x_arr[6]
    
### Start plotting

bins = np.arange(0,5,0.1)
time_bins=np.arange(0,0.4,0.01)

fig=plt.figure(figsize=(12, 20))

for i,value in enumerate(['x_err','y_err','z_err','rms']):
    ax = plt.subplot(4, 1, i+1)
    if value=='rms':
        ax.hist(eval(value),time_bins,color='0.75')
        ax.set_xlabel(value+' [s]')
    else:
        ax.hist(eval(value),bins,color='0.75')
        ax.set_xlabel(value+' [km]')
    ax.set_ylabel("Events")

fig.savefig(re.sub(".xyz",".png",input_file))


