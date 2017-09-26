#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 10:41:09 2017

@author: baillard

"""

import argparse

### Parse arguments

parser = argparse.ArgumentParser(description='Parse arguments from a GMT string of options')

parser.add_argument("GMT_opt", type=str,
                    help="GMT string containing options")

parser.add_argument("GMT_want", type=str,
                    help="String containing wanted options e.g. 'W,C'")

args = parser.parse_args()
GMT_opt=args.GMT_opt
GMT_want=args.GMT_want

### Read

GMT_opt=' '+GMT_opt
GMT_want=GMT_want.split(',')
GMT_outopt=[]

for value in GMT_want:
    scra_1=GMT_opt.split(' -'+value)
    if len(scra_1)==1:
        continue
    
    scra_1=scra_1[1]
    scra_2=scra_1.split(' ')[0]

    cmd='-'+value+scra_2
    GMT_outopt.append(cmd)
    
GMT_outopt=' '.join(GMT_outopt)

print(GMT_outopt)