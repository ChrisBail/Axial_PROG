#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 16:06:51 2017

@author: baillard

Script to plot some slice

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

### Parameters

vp_ini='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/ref_3D_mod1.dat'
vs_ini='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/ref_3D_mod2.dat'

vp_dv='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/data/dv_v11.dat'
vs_dv='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/data/dv_v21.dat'


VP=VGrid()
VS=VGrid()
DVP=VGrid()
DVS=VGrid()

VP.read(vp_ini,'lotos')
VS.read(vs_ini,'lotos')

DVP.read(vp_dv,'lotos')
DVS.read(vs_dv,'lotos')

### Perform vpvsratio

R_INI=copy.deepcopy(VP)
R_ITER=copy.deepcopy(DVP)
VAR=copy.deepcopy(VP)
VAR_P=copy.deepcopy(VP)
VAR_S=copy.deepcopy(VP)


R_INI.data[:,3]=VP.data[:,3]/VS.data[:,3]
R_ITER.data[:,3]=(VP.data[:,3]+DVP.data[:,3])/(VS.data[:,3]+DVS.data[:,3])

VAR.data[:,3]=(R_ITER.data[:,3]/R_INI.data[:,3]-1)*100

VAR_P.data[:,3]=((VP.data[:,3]+DVP.data[:,3])/VP.data[:,3]-1)*100
VAR_S.data[:,3]=((VS.data[:,3]+DVS.data[:,3])/VS.data[:,3]-1)*100

#### Write for multiple slices

for z in np.linspace(0,4,9):
    output_file=('vpvs_slice_z_%02d_km.txt'%(z*10))
    slice_param=('z=%.1f'%(z))
    print(output_file)
    VAR.write_slice(slice_param,output_file)
    
for z in np.linspace(0,4,9):
    output_file=('vp_slice_z_%02d_km.txt'%(z*10))
    slice_param=('z=%.1f'%(z))
    print(output_file)
    VAR_P.write_slice(slice_param,output_file)
    
for z in np.linspace(0,4,9):
    output_file=('vs_slice_z_%02d_km.txt'%(z*10))
    slice_param=('z=%.1f'%(z))
    print(output_file)
    VAR_S.write_slice(slice_param,output_file)







