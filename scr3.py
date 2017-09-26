#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:09:28 2017

@author: baillard
"""

import importlib
import LOTOS_class
import os
import numpy as np
importlib.reload(LOTOS_class)
from LOTOS_class import Catalog
import matplotlib.pyplot as plt


data_path='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_03/data/'

os.listdir(data_path)

### Get list of ray files
 
file_list=[]

for file in os.listdir(data_path):
    if file.startswith('rays') and file.endswith('.dat'):
        file_list.append(data_path+file)
        
file_list.sort()

### Start processing through ray file

mean_p=[]
mean_s=[]
std_p=[]
std_s=[]
it=list(range(0,len(file_list)))

for file in file_list:
    A=Catalog()
    A.read(file,'bin')
    vals=A.get_stat(type_stat='abs')[0]
    
    mean_p.append(vals['mean_P'])
    mean_s.append(vals['mean_S'])
    std_p.append(vals['std_P'])
    std_s.append(vals['std_S'])
    
### Plot with bars

fig=plt.figure()
fig.suptitle('Residuals evolution')
ax = fig.add_subplot(111)

ax.errorbar(it, mean_p, std_p,fmt='o')

ax.set_xlim([0,len(it)])
ax.set_ylim([0,max(mean_p[1:])*1.1])
    
ax.errorbar(it, mean_s, std_s,color='r',fmt='o')

ax.set_xlim([0,len(it)])
ax.set_ylim([0,max(mean_s[1:])+max(std_s[1:])])

ax.set_ylabel('Absolute residuals [s]')
ax.set_xlabel('Iteration #')

    
    



