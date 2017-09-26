#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script is made convert nonlinloc buff grid into ascii file and cross section ascii file

:param buff_file: binary nlloc binary (4 bytes float=32) file
:type buff_file: str
:param nlloc_control: nlloc control file to be used to read increment and grid size
:type nlloc_control: str
:param flag_param: flag to write cube into ascii file (0 or 1)
:type flag_param: int
:param cross_param: define x,y or z slice in the form 'x=14' (optional), cross grid will be written in a grd file and ascii name cross+extension
:type cross_param: str

example ./convert_buf.py NLLOC_AXIAL/model/layer_1D_axial.P.mod.buf NLLOC_AXIAL/run/axial_nlloc_control.in 0 x=10
 
Created on Fri Apr 14 13:35:41 2017

@author: baillard
"""

import numpy as np
from subprocess import call,check_output,PIPE,Popen
import sys


### Read command line

# Parse command line

if len(sys.argv)<4:
    print 'Not enough arg, at least 3'
    sys.exit()
elif len(sys.argv)>5:
    print 'Too many arg'
    sys.exit()

params=sys.argv[1:]

[buff_file,nlloc_control,flag_param]=params[0:3]
if len(params)==4:
    cross_param=params[3]


### Parameters

#buff_file='/home/baillard/Dropbox/_Moi/Projects/Axial/PROG/NLLOC_AXIAL/model/layer_1D_axial.P.mod.buf'
#nlloc_control='/home/baillard/Dropbox/_Moi/Projects/Axial/PROG/NLLOC_AXIAL/run/axial_nlloc_control.in'
#grid_param='300  300  150  0.0 0.0 1.40 0.05 0.05 0.05'
output_file='cube.txt'
cross_name='cross'
cross_ascii=cross_name+'.txt'
cross_grid=cross_name+'.grd'

flag_ascii=int(flag_param)

### Retrieve grid parameters from control file

shell_cmd='grep VGGRID %s' %(nlloc_control)
grid_param=check_output(shell_cmd,shell=True)

### Read binary file

val_array = np.fromfile(buff_file, dtype=np.float32)
print len(val_array)

### Process

grid_val=grid_param.split()
[num_x,num_y,num_z]=[int(i) for i in grid_val[1:4]]
[x_o,y_o,z_o,dx,dy,dz]=[float(i) for i in grid_val[4:10]]
d_step=np.array([dx,dy,dz])

### Loop to create ascii

### Great grid values

x_array=np.arange(x_o,x_o+num_x*dx, dx)
y_array=np.arange(y_o,y_o+num_y*dy, dy)
z_array=np.arange(z_o,z_o+num_z*dz, dz)


foc=open(output_file,'wt')

k=0
M = np.empty((num_x*num_y*num_z, 4));
for x in x_array:
    for y in y_array:
        for z in z_array:
            if flag_ascii:
                foc.write("%10.3f %10.3f %10.3f %10.3f \n" % (x,y,z,val_array[k]))
        
            dat=np.array([x, y, z, val_array[k]])
            M[k]=dat
            k=k+1
        
foc.close()

### Choose section 

[cross_dir,cross_val_str]=cross_param.split('=')
cross_val=float(cross_val_str)

if cross_dir.lower() == 'x':
    col_cross=0
elif cross_dir.lower() == 'y':
    col_cross=1
elif cross_dir.lower() == 'z':
    col_cross=2

### Select the right column

if col_cross==0: 
    if (cross_val<x_array[0] or cross_val>x_array[-1]):
        print 'x val out of range'
        cross_val=x_array[0]
    else:
        id_val = (np.abs(x_array-cross_val)).argmin()
        cross_val=x_array[id_val]
elif col_cross==1: 
    if (cross_val<y_array[0] or cross_val>y_array[-1]):
        print 'y val out of range'
        cross_val=y_array[0]
    else:
        id_val = (np.abs(y_array-cross_val)).argmin()
        cross_val=y_array[id_val]
elif col_cross==2: 
    if (cross_val<z_array[0] or cross_val>z_array[-1]):
        print 'z val out of range'
        cross_val=z_array[0]
    else:
        id_val = (np.abs(z_array-cross_val)).argmin()
        cross_val=z_array[id_val]

### Remove proper column
ind_select=np.array([x for x in range(4) if x!=col_cross])

### Select Plane
ii=np.where(M[:,col_cross]==cross_val)[0]
I,J=np.ix_(ii,ind_select)
cross_array=M[I,J]


### Write cross file
foc=open(cross_ascii,'wt')
for i,num in enumerate(cross_array):
    foc.write('%10.3f %10.3f %10.3f\n'%(cross_array[i,0],cross_array[i,1],cross_array[i,2]))
    
foc.close()

### Transform to grid file
sel_step=d_step[ind_select[0:2]]

gmt_cmd='gmt xyz2grd %s -G%s -R%.3f/%.3f/%.3f/%.3f -I%.3f/%.3f' \
    %(cross_ascii,cross_grid,min(cross_array[:,0]),max(cross_array[:,0]),\
      min(cross_array[:,1]),max(cross_array[:,1]),\
      sel_step[0],sel_step[1])
    
call(gmt_cmd,shell=True)

### Plot Grid file

gmt_cmt='plot_nlloc_SLICE.sh %s' %(cross_grid)

call(gmt_cmt,shell=True)