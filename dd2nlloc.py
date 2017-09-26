#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:35:11 2017

@author: baillard
"""

import numpy as np
from read_DD import read_DD
from util import weight2error
from obspy.core.event import read_events

### Parameters

dd_file='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/Axial_hypoDDPhaseInput_20150201_20150210.dat'
nlloc_file='20150201_20150210.nlloc'
network_code='OO'
format_out='NLLOC_OBS'


### Read/write

Catalog=read_DD(dd_file,network_code)


foc_global=open(nlloc_file, 'wt') 
for ev in Catalog:

    ev.write(foc_global,format=format_out)
    foc_global.write('\n')

foc_global.close()


