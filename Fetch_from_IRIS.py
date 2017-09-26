# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import obspy
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.mass_downloader import RectangularDomain, \
    Restrictions, MassDownloader, GlobalDomain

## Parameters:
    
network_code="OO"
center="IRIS"
domain = GlobalDomain()

#stations_list=["AXAS1","AXAS2","AXBA1","AXCC1","AXEC1","AXEC2","AXEC3","AXID1"]
stations_list="AX*"
client = Client(center)



### Restrictions

restrictions = Restrictions(
starttime=obspy.UTCDateTime(2015, 1, 1),
    endtime=obspy.UTCDateTime(2016, 1, 1),
    chunklength_in_sec=86400,
    network=network_code, station=stations_list, 
    # The typical use case for such a data set are noise correlations where
    # gaps are dealt with at a later stage.
    reject_channels_with_gaps=False,
    # Same is true with the minimum length. All data might be useful.
    minimum_length=0.0,
    channel_priorities=["HH[ZNE]", "EH[ZNE]"],
    # Guard against the same station having different names.
    minimum_interstation_distance_in_m=0.0
)


### Downlaod Data 


mdl=MassDownloader(providers=[center])
mdl.download(domain,restrictions,mseed_storage="/home/baillard/waveforms/",stationxml_storage='/home/baillard/')

