#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 10:47:20 2017

@author: baillard

Program made to convert nlloc to xyz file, outputs are comma separated to allow empty fields assignation
"""
import obspy
import importlib
importlib.reload(obspy.io.nlloc.core)
from obspy.core.event import read_events
import re
from obspy.geodetics import kilometer2degrees,degrees2kilometers
import sys

#from read_DD import read_DD
### Read command line
### Parameters


file_nlloc='/home/baillard/Dropbox/_Moi/Projects/Axial/PROG/NLLOC_AXIAL/loc/axial.sum.grid0.loc.hyp'
file_nlloc=sys.argv[1]
#file_nlloc='/home/baillard/Dropbox/_Moi/Projects/Axial/PROG/NLLOC_AXIAL/loc/axial.20150202.234656.grid0.loc.hyp'

### Read

Cat_nlloc=read_events(file_nlloc,format='NLLOC_HYP')

### Loop and print

for event in Cat_nlloc:
    lon=event.origins[0].longitude
    lat=event.origins[0].latitude
    depth=event.origins[0].depth/1000
    x_err=degrees2kilometers(event.origins[0].longitude_errors.uncertainty)
    y_err=degrees2kilometers(event.origins[0].latitude_errors.uncertainty)
    z_err=event.origins[0].depth_errors.uncertainty/1000
    time=event.origins[0].time
    rms=event.origins[0].quality.standard_error
    if hasattr(Cat_nlloc[0],'magnitude')==False:
        mag=999
    else:
        mag=999
    
    ### Print
    
    print(\
          "%10.4f %10.4f %7.3f %s %6.2f %7.3f %7.3f %7.3f %7.3f"\
          %(lon,lat,depth,time,mag,x_err,y_err,z_err,rms)\
          )
    
    
    

