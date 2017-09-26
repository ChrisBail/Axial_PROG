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
file_list=file_list[1:]

### Start processing through ray file

mean_p=[]
mean_s=[]
std_p=[]
std_s=[]
it=list(range(1,len(file_list)+1))

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
ax = fig.add_subplot(211)

ax.errorbar(it, mean_p, std_p,fmt='o')

ax.set_xlim([0,len(it)])
ax.set_ylim([0,max(mean_p[1:])*1.1])
    
ax.errorbar(it, mean_s, std_s,color='r',fmt='o')

ax.set_xlim([0,len(it)+1])
ax.set_ylim([0,max(mean_s[1:])+max(std_s[1:])])

ax.set_ylabel('Absolute residuals [s]')
ax.set_xlabel('Iteration #')

### Add table

clust_data=np.vstack((it,mean_p,std_p,mean_s,std_s)).transpose()
clust_data=np.around(clust_data,3)
coll_label=('iter','mean_P','std_P','mean_S','std_S')

ax_t = fig.add_subplot(212)
ta=ax_t.table(cellText=clust_data,colLabels=coll_label,loc='center',fontsize='40')
ax_t.axis('tight')
ax_t.axis('off')
ta.set_fontsize(12)

### Save figure


    



