#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:40:24 2017

@author: baillard

function...
"""

from obspy import UTCDateTime, read
from obspy.core.event import Event, Origin, Magnitude, Comment, Catalog
from obspy.core.event import EventDescription, CreationInfo, OriginQuality
from obspy.core.event import Pick, WaveformStreamID, Arrival, Amplitude


### Parameter

pick_file='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/picks.dat'
network_code='OO'
time_origin=UTCDateTime(2010,1,1,0,0,0)
new_event=Event()
new_origin=Origin()
_method_id='K'
_evaluation_mode='automatic'

### Start script

fic=open(pick_file,'r')
pick_lines = fic.read().splitlines()

for line in pick_lines:
    ### Parse line
    _station_code=line[1:6].strip()
    tt=float(line[7:14])
    weight=float(line[14:18])
    _phase_hint=line[19:21].strip()
    
    abs_time=time_origin+tt
    
    _waveform_id = WaveformStreamID(station_code=_station_code)
    
    ### Put into Pick object
    
    pick=Pick(waveform_id=_waveform_id, phase_hint=_phase_hint,
                   time=abs_time, method_id=_method_id, evaluation_mode=_evaluation_mode)
    
    ### Rename pick ID
    
    _pick_id=pick.time.isoformat()+'-'+str(pick.method_id)+'-'+pick.phase_hint+'-'+\
    pick.waveform_id.get_seed_string()
    pick.resource_id=_pick_id
    
    ### Put into Arrival object
    
    arrival=Arrival(pick_id=pick.resource_id, phase=pick.phase_hint)
    arrival.time_weight=weight
    
    ### Append to event
    

    new_event.picks.append(pick)
    
#    return new_event
    
