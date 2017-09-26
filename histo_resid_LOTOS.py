#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:11:27 2017

@author: baillard

Program made to read and plot residuals from the LOTOS
data/resid?.dat file
"""

import numpy as np
import matplotlib.pyplot as plt

input_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/data/resid1.dat'
title_text=input_file.split('/')[-1]
output_figure=title_text.split('.')[0]

### Read file and put everything into an array

fic=open(input_file,'rt')
lines=fic.read().splitlines()
fic.close()

resid_p=np.array([])
resid_s=np.array([])


for line in lines:
    A=[float(x) for x in line.split()]
    if len(A)==4:
        continue
    phase=A[0]
    station=A[1]
    resid=A[2]
    
    if phase==1:
        resid_p=np.append(resid_p,resid)
    else:
        resid_s=np.append(resid_s,resid)
        
    
mean_p=np.mean(resid_p)
std_p=np.std(resid_p)
two_sigma_p=((np.percentile(resid_p,97.72)-np.percentile(resid_p,2.28))-mean_p)/2
        
mean_s=np.mean(resid_s)
std_s=np.std(resid_s)
two_sigma_s=((np.percentile(resid_s,97.72)-np.percentile(resid_s,2.28))-mean_s)/2

### figure

fig=plt.figure(figsize=(12, 20))
fig.suptitle('Time residuals for file: {}'.format(title_text), fontsize=16)
xbins=np.linspace(-0.3,0.3,30)

ax = plt.subplot(2, 1,1)
ax.hist(resid_p,xbins,color='0.75')
ax.text(0.1, 0.8, 'mean = {:.3f}\n$\sigma$ = {:.3f}\n$2\sigma$ = {:.3f}'.format(mean_p,std_p,two_sigma_p),transform=ax.transAxes,horizontalalignment='left')
ax.set_xlabel('P Residuals [s]')
ax.set_ylabel('Number obs')
ax.set_xlim(xbins[0],xbins[-1])
ax = plt.subplot(2, 1,2)
ax.hist(resid_s,xbins,color='0.75')
ax.text(0.1, 0.8, 'mean = {:.3f}\n$\sigma$ = {:.3f}\n$2\sigma$ = {:.3f}'.format(mean_s,std_s,two_sigma_s),transform=ax.transAxes,horizontalalignment='left')
ax.set_ylabel('Number obs')
ax.set_xlabel('S Residuals [s]')
ax.set_xlim(xbins[0],xbins[-1])

fig.savefig(output_figure)
    

    
