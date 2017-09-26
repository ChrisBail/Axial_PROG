#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:29:50 2017

@author: baillard
File meant to write rays0 txt file into binary files LOTOS

"""

import numpy as np
import sys
from util import ll2xy

#input_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/MERAPI_1/MODEL_01/data/rays0.txt'

input_file=sys.argv[1]
output_file=sys.argv[2]
flag_option=False
if len(sys.argv)==4:
    flag_option=True
    try:
        geo_ref=[float(x) for x in sys.argv[3].split(',')]
        lon0,lat0=geo_ref[0],geo_ref[1]
    except ValueError:
        print('reference should be given like lon0,lat0')
        sys.exit()
    

### Open files

fac=open(output_file,'wb')

### Read file and put everything into an array

fic=open(input_file,'rt')
lines=fic.read().splitlines()
fic.close()

data=np.array([])
k=0
while k < len(lines):
    line=lines[k]
    elements=np.array([float(x) for x in line.split()])

    if flag_option:
        x,y=ll2xy(elements[0],elements[1],lon0,lat0)
        coordinates=np.array([x,y,elements[2]])
    else:
        coordinates=elements[0:3]
    coordinates.astype(dtype=np.float32).tofile(fac)
    np.array(elements[3]).astype(dtype=np.int32).tofile(fac)
    num_line=1
    tot_line=elements[3]
    k=k+1
    while num_line<=tot_line:
        line=lines[k]
        elements=np.array([float(x) for x in line.split()])
        type_pha=int(elements[0])
        num_sta=int(elements[1])
        t_obs=elements[2]
        t_ref=elements[3]
        ### Write 
        np.array(type_pha).astype(dtype=np.int32).tofile(fac)
        np.array(num_sta).astype(dtype=np.int32).tofile(fac)
        np.array(t_obs).astype(dtype=np.float32).tofile(fac)
        np.array(t_ref).astype(dtype=np.float32).tofile(fac)
        k=k+1
        num_line=num_line+1
        


### Close files

fac.close()

