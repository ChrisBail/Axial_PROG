#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:06:19 2017

@author: baillard
"""
from obspy import UTCDateTime
import matplotlib.pyplot as plt
import numpy as np
import math
import pylab
import re
from util import readxyz
from obspy.geodetics import kilometer2degrees,degrees2kilometers

### Parameters

dd_file='dd.xyz'
nlloc_file='nlloc_20m_GAU.xyz'


### Read

dd_data=readxyz(dd_file)
nlloc_data=readxyz(nlloc_file)

###

fig=plt.figure(figsize=(12, 20))
fig.suptitle('(Inversion - Grid) location differences', fontsize=20)
xbins=np.arange(-4,4,0.1)

ax = plt.subplot(3, 1,1)
ax.hist(degrees2kilometers(dd_data[0]-nlloc_data[0]),xbins,color='0.75')
ax.set_xlabel('X diff [km]')
ax = plt.subplot(3, 1,2)
ax.hist(degrees2kilometers(dd_data[1]-nlloc_data[1]),xbins,color='0.75')
ax.set_xlabel('Y diff [km]')
ax = plt.subplot(3, 1,3)
ax.hist(dd_data[2]-nlloc_data[2],xbins,color='0.75')
ax.set_xlabel('Z diff [km]')

fig.savefig("loc_diff.png")

#plt.hist(dd_data[2]-nlloc_data[2],xbins)

#plt.hist(dd_data[2],50)
