#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:22:28 2017

@author: baillard

Function made to read a phase file formatted for hypoDD, the file looks like

# 2015  1 22  0  8 58.891   45.94934 -129.99501  0.000  0.0  0.210  0.156  0.093  20831
 AXCC1  0.489 0.75 P
 AXEC1  0.569 1.00 P

"""

from obspy import UTCDateTime
from obspy.core.event import Event, Origin, Magnitude, Catalog
from obspy.core.event import QuantityError,OriginQuality
from obspy.core.event import Pick, WaveformStreamID, Arrival
from util import weight2error

def read_DD(event_file,network_code):
        
    """
    Read hypoDD
    """
    ### Parameters
    
    
    #event_file='/home/baillard/Dropbox/_Moi/Projects/Axial/DATA/test.dat'
    
    ### Start process
    
    f=open(event_file, 'r') 
    catalog = Catalog()
    
    k=0
    for line in f:
        k=k+1
        if line[0]=='#':
            if k>1:
                catalog.events.append(new_event)
            new_event=read_header_line(line)
        else:
            read_pick_line(line,new_event,network_code)
    
    ### Append last event when eof reacehd
    
    catalog.events.append(new_event)
    f.close()
    
    return catalog
    
    
def read_header_line(string_line):
    
    new_event=Event()
    line=string_line
    
    param_event=line.split()[1:]
    
    ### check if line as required number of arguments
    
    if len(param_event)!=14:
        return new_event
        
    ### Get parameters
    
    year,month,day=[int(x) for x in param_event[0:3]]
    hour,minu=[int(x) for x in param_event[3:5]]
    sec=float(param_event[5])
    if sec>=60:
        sec=59.999
    lat,lon,z=[float(x) for x in param_event[6:9]]
    mag=float(param_event[9])
    errh,errz,rms=[float(x) for x in param_event[10:13]]
    
    _time=UTCDateTime(year,month,day, hour,minu,sec)
    _origin_quality=OriginQuality(standard_error=rms)
    
            
    # change what's next to handle origin with no errors estimates
    
    origin=Origin(time=_time,
                  longitude=lon,latitude=lat,depth=z,
                  longitude_errors=QuantityError(uncertainty=errh),
                  latitude_errors=QuantityError(uncertainty=errh),
                  depth_errors=QuantityError(uncertainty=errz),
                  quality=_origin_quality)
    
    magnitude=Magnitude(mag=mag,origin_id=origin.resource_id)
    
    ### Return
    
    new_event.origins.append(origin)
    new_event.magnitudes.append(magnitude)
    new_event.preferred_origin_id=origin.resource_id
    new_event.preferred_magnitude_id=magnitude.resource_id

    return new_event
    

def read_pick_line(string_line,new_event,_network_code):

    time_origin=new_event.origins[0].time
    _method_id='K'
    _evaluation_mode='automatic'
    time_error_ref=[0.5,0.25,0.1,0.01] # translate weight into time uncertainty
    
    ### Start script
    
    line=string_line
    
    ### Parse line

    _station_code=line[1:6].strip()
    tt=float(line[7:14])
    weight=float(line[14:18])
    _phase_hint=line[19:21].strip()
    
    abs_time=time_origin+tt
    
    _waveform_id = WaveformStreamID(network_code=_network_code,station_code=_station_code)
    
    ### Put into Pick object
    
    _time_errors=weight2error(weight,time_error_ref)
    pick=Pick(waveform_id=_waveform_id, phase_hint=_phase_hint,
                   time=abs_time, method_id=_method_id, evaluation_mode=_evaluation_mode,time_errors=_time_errors)
    
    
    ### Put into Arrival object
    
    arrival=Arrival(pick_id=pick.resource_id, phase=pick.phase_hint)
    arrival.time_weight=weight
    
    ### Append to event
    
    new_event.picks.append(pick)
    new_event.origins[0].arrivals.append(arrival)
        
    return new_event

if __name__ == '__main__':
    main()
            
