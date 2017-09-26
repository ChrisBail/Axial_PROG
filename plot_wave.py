#!/usr/bin/env obspy
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:39:35 2017

@author: baillard

Functions made to plotting waveforms specifying the SDS root path
"""

import re
import sys 
import os
import numpy as np
from obspy import read_inventory
import pickle
sys.path.append(os.path.abspath("/media/baillard/Shared/Dropbox/_Moi/Projects/Axial/PROG"))
from read_DD import *
from util import * 
from obspy.core.event import read_events
from obspy.core.event import Event
from obspy.clients.filesystem.sds import Client as sds_client
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



### Parameters

event_file='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/CATALOG/201501.xml'
sds_root='/home/baillard/SDS/'
stationxml="/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/STATIONS/AXIAL_stations.xml"
time_delay=20 # time in seconds
_network_code='OO'
_station_code='A*'
_location_code='*'
_channel_code='[E|H]H*'
pick_colormap={'P':'k','S':'r'}



### Read Event

catalog = read_events(event_file) 
single_event=catalog[8]

### Check if type is correct

if type(single_event) is not type(Event()):
    raise Exception('Event given is not and obspy Event')

### Read Station xml

inv=read_inventory(stationxml,format="STATIONXML")

### Read SDS client

client=sds_client(sds_root,sds_type='D',format='MSEED')

### Read starttime from preferred origin

origin_pref=[x for x in single_event.origins if x.resource_id==single_event.preferred_origin_id][0]
arrivals_pref=origin_pref.arrivals
_starttime=origin_pref.time-10
_endtime=_starttime+time_delay

st= client.get_waveforms(_network_code,_station_code,_location_code,_channel_code,_starttime,_endtime)

### Pre-process streams

st.sort(keys=['network','station','channel'])
st.taper(type="cosine",max_percentage=0.1)
st.filter("bandpass",freqmin=3,freqmax=50,corners=4)

#st.plot(starttime=origin_pref.time, endtime=origin_pref.time+3, fig=fig2)

### Start plotting waveforms 


fig=plt.figure(figsize=(20, 12))

wave_ids=[x.get_id() for x in st.traces]
station_list=list(set([x.split('.')[1] for x in wave_ids]))
st_num=len(st)
axs=[]

for i,tr in enumerate(st):
    net, sta, loc, cha = tr.id.split(".")
    if loc=='':
            loc=None

    starttime_relative=tr.stats.starttime-_starttime
    sampletimes = np.arange(starttime_relative,
            starttime_relative + (tr.stats.delta * tr.stats.npts),
            tr.stats.delta)

    if len(sampletimes) == tr.stats.npts + 1:
        sampletimes = sampletimes[:-1]

    if i == 0:
        ax = fig.add_subplot(st_num, 1, i+1)
    else:
        ax = fig.add_subplot(st_num, 1, i+1, sharex=axs[0])

    axs.append(ax)
    ax.plot(sampletimes,tr.data)
    ### Add label
    ax.text(0.1, 0.90, tr.id, transform=ax.transAxes)

fig.subplots_adjust(hspace=0)
axs[0].set_xlim(0,sampletimes[-1])

### Plot Picks on top of the waveforms

picks=single_event.picks
arrivals=single_event.origins[0].arrivals

# Select picks that are in arrivals

picks_sel=[getPickForArrival(picks, arrival) for arrival in arrivals]
    
for i,tr in enumerate(st):
    ax=axs[i]
    net,sta,loc,chan=tr.id.split('.')
    if net=='':
        net=None
    if sta=='':
        continue
    if loc=='':
        loc=None
    print sta
    picks_tr=getPicks(picks_sel,net,sta,loc)
    for pick_tr in picks_tr:
        phase_pick=pick_tr.phase_hint
        rel_time_pick=pick_tr.time-_starttime
        ax.axvline(x=rel_time_pick, ymin=0, ymax=1,color=pick_colormap[phase_pick],lw=2)
        

#for ind,wave_id in enumerate(wave_ids):
#    
#    
#
#for ind_wave,wave_id in enumerate(wave_ids):
#    
#for ind_sta,station in enumerate(station_list):
#    sel_wave_ids=[x for x in wave_ids if x.split('.')[1]==station]
#
#    for ind_trace,trace_id in enumerate(sel_wave_ids):
#
#        select_trace=st.select(id=trace_id)[0]
#        select_trace.plot(fig=fig3)
#        
#
#fig3.show()

#
#if __name__ == '__main__':
#    main()
#            