#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:42:28 2017

@author: baillard
"""

import numpy as np

torad=np.pi/180

teta=160
teta=teta*torad
W=4
L1=0
L2=8

x=np.array([0,0,-W/2,-W/2,W/2,W/2])

y=np.array([-L1, L2, -L1, L2, L2,-L1])

coord= np.stack((x, y), axis=-1)

rotmat=np.array([[np.cos(teta), np.sin(teta)],[-np.sin(teta) ,np.cos(teta)]])

##Apply rotation

new_coord=np.dot(rotmat,np.transpose(coord))

new_x=new_coord[0,:]
new_y=new_coord[1,:]