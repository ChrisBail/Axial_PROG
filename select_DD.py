#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:22:47 2017

@author: baillard

Function made to select events from a dd file of the type:
    
# 2015  1 31 23 59 16.394   45.95409 -129.99374  1.134 -0.0  1.014  1.746  0.035  28271
 AXCC1  0.451 1.00 P
 AXEC1  0.506 0.50 P
 AXEC2  0.656 1.00 P
 AXEC3  0.681 1.00 P
 AXAS1  0.311 0.00 P
 AXCC1  1.061 0.25 S
 AXEC1  0.941 0.33 S
 AXEC2  1.291 0.33 S
 
The selection is made on different paramters such as:
    the RMS, the depth, lon, lat, num of P-phases....
    
Input: DD_file
Output: DD_file with selected events

A log file called select.log is also outputted with stats
    
"""

import numpy as np
import sys
from read_DD import read_DD 
from util import getPickForArrival

### Parameters

input_dd='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/Axial_hypoDDPhaseInput_20150201_20150210.dat'
input_dd='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/Axial_hypoDDPhaseInput.dat'
network_code='OO'

### Conditions to meet

cond_rms=0.1  # RMS minimum (for the whole event)
min_w_P=0.4  # min P weight to keep the obs
min_w_S=0.2  # min S....
min_num_P=6 # min number of P-phase to keep the event
min_num_S=5 # ......S-phase...
lon_range=[-130.1, -129.9] # Geo range conditions
lat_range=[45.9, 46]
z_range=[0,7]

### Read

Catalog=read_DD(input_dd,network_code)

### Read header lines for storing (easier than rewriting the line)

fic=open(input_dd,'rt')
lines=fic.read().splitlines()
header_lines=[line for line in lines if line[0]=='#']
fic.close()

### Open log file

fic=open('select.log','wt')

### Check

if len(header_lines)!=len(Catalog):
    print('Problem in the number of lines')
    sys.exit()
    
### Statisics

num_ev_keep=0
num_ev_rej=0
num_P_keep=0
num_P_rej=0
num_S_keep=0
num_S_rej=0
mean_rms=0
tot_P=0
tot_S=0

### Start selecting

count_ev=0

for ev in Catalog:
    count_ev=count_ev+1
    lon=ev.origins[0].longitude
    lat=ev.origins[0].latitude
    depth=ev.origins[0].depth
    num_phase=len(ev.origins[0].arrivals)
    rms=ev.origins[0].quality.standard_error
    
    picks=ev.picks
    t0=ev.origins[0].time
    
    tot_P_ev=sum([1 for arrival in ev.origins[0].arrivals if arrival.phase=='P'])
    tot_S_ev=sum([1 for arrival in ev.origins[0].arrivals if arrival.phase=='S'])
    
    tot_P=tot_P+tot_P_ev
    tot_S=tot_S+tot_S_ev
    
    ### First conditions
    
    if not (lon_range[0]<= lon <= lon_range[1] and lat_range[0]<= lat <= lat_range[1] and
            z_range[0]<= depth <= z_range[1]):
        fic.write('Event n° %5i rejected; Not in geo range\n'%(count_ev))
        continue
    
    if not (rms<=cond_rms):
        fic.write('Event n° %5i rejected; rms bigger than limit\n'%(count_ev))
        continue
    
    ### Second conditions
    
    num_P_keep_ev=0
    num_S_keep_ev=0
    k_P_rej=[]
    k_S_rej=[]
    phase_bloc=''

    
    for i,arrival in enumerate (ev.origins[0].arrivals):
        pick=getPickForArrival(picks, arrival)
        station=pick.waveform_id.station_code
        phase=arrival.phase
        weight=arrival.time_weight
        time_pick=pick.time
        tt=time_pick-t0
        phase_line='%6s%7.3f%5.2f %1s'%(station,tt,weight,phase)

        if phase=='P' and weight>=min_w_P:
            num_P_keep_ev +=1
            phase_bloc=phase_bloc+'\n'+phase_line
            
        if phase=='S' and weight>=min_w_S:
            num_S_keep_ev +=1
            phase_bloc=phase_bloc+'\n'+phase_line

    ### check number of phases to see if we print
        
    if not (num_P_keep_ev>= min_num_P and num_S_keep_ev>= min_num_S ):
        fic.write('Event n° %5i rejected; not enough P or S phases\n'%(count_ev))
        continue
        
    num_P_keep=num_P_keep+num_P_keep_ev
    num_S_keep=num_S_keep+num_S_keep_ev
    num_ev_keep=num_ev_keep+1
    
    ### Start printing to terminal
        
    print(header_lines[count_ev-1])
    print(phase_bloc[1:])
            
        
### Write stats

fic.write('Number of events rejected:%i\n'%(count_ev-num_ev_keep))
fic.write('Number of events kept:%i\n'%(num_ev_keep))
fic.write('Number of P phase kept %.2f %% (total=%i)\n'%( (num_P_keep/tot_P)*100,tot_P ))
fic.write('Number of S phase kept %.2f %% (total=%i)\n'%( (num_S_keep/tot_S)*100,tot_S ))

fic.close() # Close log file