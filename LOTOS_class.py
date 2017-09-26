#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:10:12 2017

@author: baillard

Program made to define the classes to read rays.txt files
"""

import numpy as np
import os
import matplotlib.pyplot as plt


### Parameters


class Catalog(object):
        
    def __init__(self):
        """
        """
        self.events=[]
        self.file=None
        
    def read(self,input_file,format_file=None):
        """
        """
        
        ### Get filename
        
        file_short=input_file.split('/')[-1]
        self.file=file_short
        
        ### Transform binary to text if necessary
        
        if format_file=='bin':
            cmd='rays2txt.py '+input_file+' > tmp_ray.txt'
            print(cmd)
            os.system(cmd)
            input_file='tmp_ray.txt'
            
        
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
        
    def get_stat(self,type_stat=None):
        
        events=self.events[:]
        resid_P_all=[]
        resid_S_all=[]
        num_P_all=0
        num_S_all=0
        
        outdict=dict()
        
        for event in events:
            resid_P,num_P,resid_S,num_S,resid_all=event.get_stat()
            num_P_all=num_P_all+num_P
            num_S_all=num_S_all+num_S
            resid_P_all.extend(resid_P)
            resid_S_all.extend(resid_S)
        
        ### Compute stat
        
        mean_P,std_P,two_sigma_P=statistics(resid_P_all,type_stat)
        mean_S,std_S,two_sigma_S=statistics(resid_S_all,type_stat)
        
        outdict.update({
                'mean_P':mean_P,'std_P':std_P,'two_sigma_P':two_sigma_P,
                'mean_S':mean_S,'std_S':std_S,'two_sigma_S':two_sigma_S,
                'num_P_all':num_P_all,'num_S_all':num_S_all
                        })
 
        ### Return 
        
        return outdict,resid_P_all,resid_S_all
        
    def plot_stat(self):
        
        ### Get stat
        
        indict,resid_p,resid_s=self.get_stat()
        
        ### Figure

        fig=plt.figure(figsize=(12, 20))
        fig.suptitle('Time residuals for file: {}'.format(self.file), fontsize=16)
        xbins=np.linspace(-0.3,0.3,30)
        
        ax = plt.subplot(2, 1,1)
        ax.hist(resid_p,xbins,color='0.75')
        ax.text(0.1, 0.8, 'mean = {:.3f}\n$\sigma$ = {:.3f}\n$2\sigma$ = {:.3f}'.format(
                indict['mean_P'], indict['std_P'],indict['two_sigma_P']),transform=ax.transAxes,horizontalalignment='left')
        ax.set_xlabel('P Residuals [s]')
        ax.set_ylabel('Number obs')
        ax.set_xlim(xbins[0],xbins[-1])
        ax = plt.subplot(2, 1,2)
        ax.hist(resid_s,xbins,color='0.75')
        ax.text(0.1, 0.8, 'mean = {:.3f}\n$\sigma$ = {:.3f}\n$2\sigma$ = {:.3f}'.format(
                indict['mean_S'], indict['std_S'],indict['two_sigma_S']),transform=ax.transAxes,horizontalalignment='left')
        ax.set_ylabel('Number obs')
        ax.set_xlabel('S Residuals [s]')
        ax.set_xlim(xbins[0],xbins[-1])
        
        #fig.savefig(output_figure)

            
def statistics(data_array,type_stat=None):

    if type_stat=='abs':
        data_array=np.abs(data_array)
        
    mean_D=np.mean(data_array)
    std_D=np.std(data_array)
    two_sigma_D=((np.percentile(data_array,97.72)-np.percentile(data_array,2.28))-mean_D)/2
        
    print('mean=%.3f,sigma=%.3f,2sigma=%.3f'%(mean_D,std_D,two_sigma_D))
    return mean_D,std_D,two_sigma_D
    
        

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
        
    def __repr__(self):
        return "X:%10.3f Y:%10.3f Z:%10.3f" % (self.x, self.y,self.z)
        
    def get_stat(self):
        
        phases=self.phases[:]
        num_P=0
        num_S=0
        
        resid_P=[]
        resid_S=[]
        resid_all=[]
        
        for phase in phases:
            resid=phase.t_obs-phase.t_tho
            resid_all.append(resid)
            if phase.type==1:
                resid_P.append(resid)
                num_P+=1
            else:
                resid_S.append(resid)
                num_S+=1
        
        return resid_P,num_P,resid_S,num_S,resid_all
            
            
        
        
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
        
    def __repr__(self):
        return "Phase:%1d Station:%3d t_obs: %10.3f t_tho: %10.3f" \
    % (self.type, self.station,self.t_obs,self.t_tho)
        
        
        



