#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:09:06 2017

@author: baillard
"""


import numpy as np
import struct
import sys
sys.path.append('./LOTOS_utilities')
import matplotlib.pyplot as plt
import scipy.interpolate 
import pickle
import time 
import LOTOS_util
import importlib
import pyproj
import vgrid
importlib.reload(LOTOS_util)
importlib.reload(vgrid)
from vgrid import VGrid
import copy


lotos_file='/media/baillard/Shared/Dropbox/_Moi/Projects/Axial/DATA/VELOCITY/3D/VGRID_x15_y15_z4_100m_1525.lotos'
vfile_1D='/media/baillard/Shared/Dropbox/_Moi/Projects/Axial/DATA/VELOCITY/AXIAL_1D_PS_model.zv'

A=VGrid()

A.read(lotos_file,'lotos')


#A.plot_slice("z=0")

border_x=[8,10]
border_y=[2,5]

####

velocities=np.array([])
depth=np.array([])

for z in np.arange(0,4,0.2):
    border_z=[z,z+0.2]
    bool_x=LOTOS_util.select_elements(A.data[:,0],border_x)
    bool_y=LOTOS_util.select_elements(A.data[:,1],border_y)
    bool_z=LOTOS_util.select_elements(A.data[:,2],border_z)
    bool_tot=bool_x & bool_y & bool_z
    velocity=A.data[bool_tot ,3]
    velocities=np.append(velocities,np.mean(velocity))    
    depth=np.append(depth,z)


### Load 1D file

data_1D=np.loadtxt(vfile_1D)

fig = plt.figure()
ax = fig.add_subplot(111)


h1,=plt.step(velocities,depth,label='3D_Adrien',linewidth=1.5)
h2,=plt.step(data_1D[:,1],data_1D[:,0],'red', label='1D_William',linewidth=1.5)

ax=plt.gca()


plt.ylim([0,4])
plt.ylabel('Depth [km]')
plt.xlabel('Vp [km/s]')
plt.gca().invert_yaxis()
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 
plt.legend(handles=[h1, h2])


plt.savefig('1D_3D.png')





