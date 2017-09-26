#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:57:08 2017

@author: baillard

Function made to read William's hypoDD phase.dat and return
a LOTOS rays.dat file, see LOTOS guide for exampleAxial_hypoDDPhaseInput_20150201_20150210_selection.dat
Stations names are converted to numbers in LOTOS
The stations are given as a string, station names are separated by commas
first argument is the input phase file
second argument is the stations string
output is redirected to command prompt
"""

import numpy as np
from read_DD import *
from util import getPickForArrival
import sys

### Parameters

dd_file='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/Axial_hypoDDPhaseInput_20150201_20150210.dat'
rays_file='20150201_20150210.rays'
network_code='OO'
station_string='AXAS1,AXAS2,AXCC1,AXEC1,AXEC2,AXEC3,AXID1'

### Read from command line

if len(sys.argv)!=3:
    print('Not enough arguments, abort!')
    sys.exit()

dd_file=sys.argv[1]
station_string=sys.argv[2]



### Split list and order it alphabitecally

station_list=sorted(station_string.split(","))
values=list(np.arange(1,len(station_list)+1))
station_dict = dict(zip(station_list, values))  # give to each stations the corresponding scalar
phase_dict=dict(zip(['P','S'],[1,2]))

### Read/write

Catalog=read_DD(dd_file,network_code)


### Write

for ev in Catalog:
    lon=ev.origins[0].longitude
    lat=ev.origins[0].latitude
    depth=ev.origins[0].depth
    num_phase=len(ev.origins[0].arrivals)
    picks=ev.picks
    t0=ev.origins[0].time
    
    ### Write into file
    print("%11.6f%16.6f%16.5f%18d"%(lon,lat,depth,num_phase))
    
    for arrival in ev.origins[0].arrivals:
        phase=arrival.phase
        pick=getPickForArrival(picks, arrival)
        time_pick=pick.time
        station=pick.waveform_id.station_code
        
        ### retrieve station number
        station_num=station_dict[station]
        
        ### retrieve phase number
        phase_num=phase_dict[phase]
        
        tt_pick=time_pick-t0 # time in seconds
        
        ### Write into file
        print("%12d%15d%12.5f"%(phase_num,station_num,tt_pick))
        
        
        

