#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:22:33 2017

@author: baillard

file made to convert lotos dv file into xyz file binary or text, converted or not

vlotos2xyz dv.lotos output.file [lon0/lat0] [txt or bin]
"""

import sys
import argparse
import importlib
sys.path.append('/media/baillard/Shared/Dropbox/_Moi/Projects/Axial/PROG/LOTOS_utilities/')
import vgrid
importlib.reload(vgrid)
from vgrid import VGrid


########## Read command line and Parse commands

parser = argparse.ArgumentParser(description='Convert LOTOS binary velocity file into a xyzv, bin or txt, file that could be read by GMT')

parser.add_argument("input_file", type=str,
                    help="LOTOS input file name")
parser.add_argument("output_file", type=str,
                    help="Output file name")

parser.add_argument("-c", "--center",type=str,
                    help="Center for converting to lon/lat, form lon0/lat0, if nothing is given then data is in x y")
parser.add_argument("-t", "--type",type=str,default='bin',choices=['bin','lotos','txt'],
                    help="Type of output, default is bin")

args = parser.parse_args()

input_file=args.input_file
output_file=args.output_file
center=args.center
type_file=args.type


if center:
    geo_ref=[float(x) for x in center.split('/')]
    lon0,lat0=geo_ref[0],geo_ref[1]

### Initialize

GRID=VGrid()

### Read lotos file

GRID.read(input_file,'lotos')

### Convert to lon/lat if center is defined


if center:
    GRID.xy2ll(lon0,lat0)

### Write lotos file in binary format to be used in GMT

GRID.write(output_file,type_file)





