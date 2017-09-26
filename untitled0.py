#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:59:35 2017

@author: baillard

Script made to compare nonlinloc sum files and returns xyz position t0 and 

"""


import obspy
import importlib
importlib.reload(obspy.io.nlloc.core)
from obspy.core.event import read_events
import re
from read_DD import read_DD

### Parameters

file_nlloc='/home/baillard/Dropbox/_Moi/Projects/Axial/PROG/NLLOC_AXIAL/loc/axial.sum.grid0.loc.hyp'
file_DD='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/Axial_hypoDDPhaseInput_20150201_20150210.dat'


#### Read catalog files

Cat_DD=read_DD(file_DD,'OO')


#format_read="%s   obs:%s   %s:v%s(%s)  run:%s"