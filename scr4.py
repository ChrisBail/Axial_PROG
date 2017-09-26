#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 13:37:13 2017

@author: baillard
"""


import numpy as np
import matplotlib.pyplot as plt
import sys
import importlib
sys.path.append('./LOTOS_utilities')
from util import is_in_circle
import vgrid
import LOTOS_util
importlib.reload(LOTOS_util)
importlib.reload(vgrid)
from vgrid import VGrid
import copy



input_file='/home/baillard/PROGRAMS/LOTOS13_unix/DATA/AXIALSEA/MODEL_04/data/stat_xy.dat'


x,y,z=np.loadtxt(input_file)