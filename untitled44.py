#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:16:34 2017

@author: baillard
"""

import importlib
import sys
sys.path.append('./LOTOS_utilities')
import vgrid
importlib.reload(vgrid)
from vgrid import VGrid
import matplotlib.pyplot as plt
import numpy as np

### Parameters

plt.close('all')

xo=np.arange(0, 10, 0.1)
yo=np.arange(0, 10, 0.1)
radius=0.5

input_file='./ref_3D_mod1.dat'
station_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_04/data/stat_xy.dat'

A=VGrid()

A.read(input_file,'lotos')
A.read_stations(station_file)

A.plot_slice('y=6')

### Retrieve velocity close to station

z_1d,v_1d,_=A.get_1D_velocity(7,6,0.1,True)

### Get 3D cube

shape_dim=tuple(A.num_elem)
v_3d=np.reshape(A.data[:,3],shape_dim)

### repeat 1D v to make a cube

v_3d_cake=A.extend_1D_velocity(v_1d)

### Operation on cubes

v_3d_new=v_3d-v_3d_cake

### Reshape to column

A.data[:,3]=np.reshape(v_3d_cake,-1)

### Plot to check

A.plot_slice('y=6')
z_1d,v_1d,_=A.get_1D_velocity(7,6,0.1,True)



#depth,vel,fout=A.get_1D_velocity(xo,yo,radius,True)


