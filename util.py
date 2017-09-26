#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:59:15 2017

@author: baillard
"""

from obspy import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt

def getPickForArrival(picks, arrival):
    """
    searches list of picks for a pick that matches the arrivals pick_id
    and returns it (empty Pick object otherwise).
    """
    pick = None
    for p in picks:
        if arrival.pick_id == p.resource_id:
            pick = p
            break
    return pick

def getPicks(picks,network, station, location):
    """
    returns all matching picks as list.
    """
    ret = []
    for p in picks:
        if network != p.waveform_id.network_code:
            continue
        if station != p.waveform_id.station_code:
            continue
        if location != p.waveform_id.location_code:
            continue
        ret.append(p)
    return ret

def weight2error(weight,time_map):
    """ Convert weight (float 0 to 1), to time error
    """
    if len(time_map)!=4:
        print('time_map must have 4 elements')
        return
    
    if weight==0:
        error=999
    elif weight>0 and weight<=0.25:
        error=time_map[0]
    elif weight>0.25 and weight<=0.5:
        error=time_map[1]
    elif weight>0.5 and weight<=0.75:
        error=time_map[2]
    elif weight>0.75 and weight<=1:
        error=time_map[3]

    return error


def readxyz(input_file):
    
    fic=open(input_file,'rt')
    
    lines=fic.read().splitlines()
    
    x_err_arr=[]
    y_err_arr=[]
    z_err_arr=[]
    rms_arr=[]
    x_arr=[]
    y_arr=[]
    z_arr=[]
    time_arr=[]
    
    for line in lines:
        elements=line.split()
        x,y,z=[float(i) for i in elements[0:3]]
        time=UTCDateTime(elements[3])
        x_err,y_err,z_err,rms=[float(i) for i in elements[5:]]
        x_err_arr=np.append(x_err_arr,x_err)
        y_err_arr=np.append(y_err_arr,y_err)
        z_err_arr=np.append(z_err_arr,z_err)
        rms_arr=np.append(rms_arr,rms)
        time_arr=np.append(time_arr,time)
        x_arr=np.append(x_arr,x)
        y_arr=np.append(y_arr,y)
        z_arr=np.append(z_arr,z)
        
    fic.close()
    
    return x_arr,y_arr,z_arr,time_arr,x_err_arr,y_err_arr,z_err_arr,rms_arr

def ll2xy(lon,lat,lon0,lat0):
    
    r=6371
    rad=np.pi/180

    lat_rad=lat*rad
    y_tmp=r*np.cos((lon-lon0)*rad)*np.cos(lat_rad)
    x=r*np.sin((lon-lon0)*rad)*np.cos(lat_rad)
    z1=r*np.sin(lat_rad)
    lat0_rad=lat0*rad
    y=-y_tmp*np.sin(lat0_rad)+z1*np.cos(lat0_rad)
    
    return x,y

def xy2ll(x,y,lon0,lat0):
    """
    Function made to convert from x,y to lon,lat given lon0 and lat0 reference
    coordinates
    """
    
    r=6371
    rad=np.pi/180
    
    z=np.sqrt(r*r-x*x-y*y)

    tet0=lat0
    fi0=lon0
    per=rad
    
    x1=x
    y1=-y*np.sin(tet0*per)+z*np.cos(tet0*per)
    z1=y*np.cos(tet0*per)+z*np.sin(tet0*per)

    if x1==0:
            fi=fi0
    else:
        if x1>0 and y1>0:
            PA=0
        elif x1<0:
            PA=-np.pi
        elif x1>0 and y1<=0:
            PA=2*np.pi
        
        ff=np.arctan(y1/x1)/per
        fi=fi0-(ff+PA/per)+90

    if fi > 360:
        fi=fi-360
        
    if np.abs(fi-fi0)>np.abs(fi-fi0-360):
        fi=fi-360
    if np.abs(fi-fi0)>np.abs(fi-fi0+360):
        fi=fi+360
    
    r=np.sqrt(x1*x1+y1*y1+z1*z1)
    tet=np.arcsin(z1/r)/per
    
    lon=fi
    lat=tet
    
    return lon,lat

def is_in_circle(x,y,xo,yo,radius,flag_plot=None):
    """
    Function made to return x,y and boolean of elements that are isinde the 
    circle of center xo and yo with radius.
    x and y are numpy array, xo and yo and radius are floats
    if flag_plot=true, we will plot elements that in the circle
    """
    
    ### Compute val
    
    val=(x-xo)*(x-xo)+(y-yo)*(y-yo)

    ### Get boolean
    
    boolean=val<=radius**2
    x_sel=x[boolean]
    y_sel=y[boolean]
    
    ### Print
    
    print('Number of elemnents selected is %i'%(len(x_sel)))
    
    if flag_plot:
        
    ### Figure
    
        plt.figure()
        plt.plot(x,y,'.',color='g')
        plt.plot(x_sel,y_sel,'.',color='r')

        plt.axis('equal')
    
        
    return x_sel,y_sel,boolean