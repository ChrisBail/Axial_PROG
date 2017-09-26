#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:28:36 2017

@author: baillard

Program made  to plot the nodes from a gr11.dat file outputted by lotos
The input file is a text file containing num_lines,y in the first record 
then x, z , nuù_ nodes in the following records. 
The locations paramaters are in km.
The program plots in 3D the node distribution

"""

import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


node_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_01/data/gr11.dat'
node_file=sys.argv[0]

### Start processing


fic=open(node_file,'rt')
lines=fic.readlines()
fic.close()


k=0

x_nodes=np.array([])
y_nodes=np.array([])
z_nodes=np.array([])
num_nodes=np.array([])


### Strat loop

while k<len(lines):
    data=[float(x) for x in lines[k].split()]

    k=k+1
    
    num_lines=data[0]
    y=data[1]
    
    n=1
    
    while n<=num_lines:
        data=[float(x) for x in lines[k].split()]
        k=k+1
        n=n+1
        if data[2]==0:
            continue
        
        x=data[0]
        z=data[1]
        num=data[2]
        x_nodes=np.append(x_nodes,x)
        y_nodes=np.append(y_nodes,y)
        z_nodes=np.append(z_nodes,z)
        num_nodes=np.append(num_nodes,num)
    
 
### Start writing into file

for i in range(len(x_nodes)):
    print('%10.4f %10.4f %10.3f %8i'%(x_nodes[i],y_nodes[i],z_nodes[i],num_nodes[i]))
    
### Start plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.axis('equal')
ax.scatter(x_nodes, y_nodes, z_nodes,c='r', marker='o')


ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')

ax.invert_zaxis()

