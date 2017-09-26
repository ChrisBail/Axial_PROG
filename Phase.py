#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:10:12 2017

@author: baillard

Program made to return the major stats of the rays.txt
"""



### Parameters


class Catalog(object):
        
    def __init__(self):
        """
        """
        self.events=[]
        
    def read(self,input_file):
        """
        """
        
        ### Read file and put everything into an array

        fic=open(input_file,'rt')
        line=1
        
        while line:
            line=fic.readline()
            if not line:
                break
            event_tmp=Event()
            self.events.append(event_tmp)
            event_tmp.read_header(line)
            phase_counter=1
     
            while phase_counter<=event_tmp.num_phase:
                line=fic.readline()
                event_tmp.phases.append(Phase(line))
                phase_counter=phase_counter+1

            
        fic.close()
        

class Event(object):
    
    def __init__(self):
        """
        """
        self.phases=[]
        self.x=None
        self.y=None
        self.z=None
        self.num_phase=None
        
    def read_header(self,header):
        
        self.x,self.y,self.z,self.num_phase=\
        [float(x) for x in header.split()]
        

class Phase(object):
    
    def __init__(self,line=None):
        """
        Define attributes
        """
        self.type=None
        self.station=None
        self.t_obs=None
        self.t_tho=None
        self.read(line)
        
    def read(self,phase_string):
        
        self.type,self.station,self.t_obs,self.t_tho=\
        [float(x) for x in phase_string.split()]
        
        



