#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:16:34 2017

@author: baillard
"""

import importlib
import sys
sys.path.append('/media/baillard/Shared/Dropbox/_Moi/Projects/Axial/PROG/LOTOS_utilities')
import vgrid
importlib.reload(vgrid)
from vgrid import VGrid
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

### Parameters

plt.close('all')

P_model='./ref_3D_mod1.dat'
S_model='./ref_3D_mod2.dat'
station_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_04/data/stat_xy.dat'

### Read files

P_ini=VGrid()
S_ini=VGrid()

P_ini.read(P_model,'lotos')
S_ini.read(S_model,'lotos')

### Compute Vp/VS

PS_ini=deepcopy(P_ini) 

PS_ini.data[:,3]=P_ini.data[:,3]/S_ini.data[:,3]

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

A.data[:,3]=np.reshape(v_3d_new,-1)

### Plot to check

A.plot_slice('y=6')
z_1d,v_1d,_=A.get_1D_velocity(7,6,0.1,True)



#depth,vel,fout=A.get_1D_velocity(xo,yo,radius,True)


