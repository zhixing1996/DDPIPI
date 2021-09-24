#!/usr/bin/env python
"""
Common tools 
"""

__author__ = "Maoqiang JING <jingmq@ihep.ac.cn>"
__copyright__ = "Copyright (c) Maoqiang JING"
__created__ = "[2019-08-13 Tue 15:05]" 

import sys 
import os, errno
import shutil
import ROOT 

# ---------------------------------------------
# Function 
# ---------------------------------------------

# parameter pull values' range
def pull_range(ecms):
    RANGE_LOW = 999.
    RANGE_UP = 999.
    BINS = 50
    if int(ecms == 4190):
        RANGE_LOW = 0.127
        RANGE_UP = 0.1295
        BINS = 50
    elif int(ecms == 4200):
        RANGE_LOW = 0.132
        RANGE_UP = 0.1345
        BINS = 50
    elif int(ecms == 4210):
        RANGE_LOW = 0.141
        RANGE_UP = 0.1445
        BINS = 50
    elif int(ecms == 4220):
        RANGE_LOW = 0.1585
        RANGE_UP = 0.1605
        BINS = 50
    elif int(ecms == 4230):
        RANGE_LOW = 0.172
        RANGE_UP = 0.1727
        BINS = 50
    elif int(ecms == 4237):
        RANGE_LOW = 0.1652
        RANGE_UP = 0.1675
        BINS = 50
    elif int(ecms == 4245):
        RANGE_LOW = 0.171
        RANGE_UP = 0.1735
        BINS = 50
    elif int(ecms == 4246):
        RANGE_LOW = 0.1625
        RANGE_UP = 0.1658
        BINS = 50
    elif int(ecms == 4260):
        RANGE_LOW = 0.1838
        RANGE_UP = 0.1858
        BINS = 50
    elif int(ecms == 4270):
        RANGE_LOW = 0.187
        RANGE_UP = 0.189
        BINS = 50
    elif int(ecms == 4280):
        RANGE_LOW = 0.1878
        RANGE_UP = 0.1894
        BINS = 50
    elif int(ecms == 4290):
        RANGE_LOW = 0.181
        RANGE_UP = 0.1824
        BINS = 50
    elif int(ecms == 4310):
        RANGE_LOW = 0.1995
        RANGE_UP = 0.2015
        BINS = 50
    elif int(ecms == 4315):
        RANGE_LOW = 0.1942
        RANGE_UP = 0.1952
        BINS = 50
    elif int(ecms == 4340):
        RANGE_LOW = 0.197
        RANGE_UP = 0.203
        BINS = 50
    elif int(ecms == 4360):
        RANGE_LOW = 0.19
        RANGE_UP = 0.25
        BINS = 20
    elif int(ecms == 4380):
        RANGE_LOW = 0.14
        RANGE_UP = 0.26
        BINS = 25
    elif int(ecms == 4390):
        RANGE_LOW = 0.18
        RANGE_UP = 0.24
        BINS = 25
    elif int(ecms == 4400):
        RANGE_LOW = 0.16
        RANGE_UP = 0.24
        BINS = 20
    elif int(ecms == 4420):
        RANGE_LOW = 0.16
        RANGE_UP = 0.26
        BINS = 20
    elif int(ecms == 4440):
        RANGE_LOW = 0.16
        RANGE_UP = 0.26
        BINS = 50
    elif int(ecms == 4470):
        RANGE_LOW = 0.21
        RANGE_UP = 0.24
        BINS = 50
    elif int(ecms == 4530):
        RANGE_LOW = 0.18
        RANGE_UP = 0.28
        BINS = 50
    elif int(ecms == 4575):
        RANGE_LOW = 0.2
        RANGE_UP = 0.3
        BINS = 20
    elif int(ecms == 4600):
        RANGE_LOW = 0.2
        RANGE_UP = 0.28
        BINS = 20
    elif int(ecms == 4610):
        RANGE_LOW = 0.2
        RANGE_UP = 0.26
        BINS = 15
    elif int(ecms == 4620):
        RANGE_LOW = 0.21
        RANGE_UP = 0.25
        BINS = 15
    elif int(ecms == 4640):
        RANGE_LOW = 0.21
        RANGE_UP = 0.25
        BINS = 15
    elif int(ecms == 4660):
        RANGE_LOW = 0.22
        RANGE_UP = 0.24
        BINS = 20
    elif int(ecms == 4680):
        RANGE_LOW = 0.22
        RANGE_UP = 0.25
        BINS = 50
    elif int(ecms == 4700):
        RANGE_LOW = 0.23
        RANGE_UP = 0.24
        BINS = 50
    elif int(ecms == 4740):
        RANGE_LOW = -0.005
        RANGE_UP = 0.005
        BINS = 50
    elif int(ecms == 4750):
        RANGE_LOW = -0.005
        RANGE_UP = 0.005
        BINS = 50
    elif int(ecms == 4780):
        RANGE_LOW = -0.002
        RANGE_UP = 0.007
        BINS = 50
    elif int(ecms == 4840):
        RANGE_LOW = -0.003
        RANGE_UP = 0.005
        BINS = 50
    elif int(ecms == 4914):
        RANGE_LOW = -0.003
        RANGE_UP = 0.005
        BINS = 50
    elif int(ecms == 4946):
        RANGE_LOW = -0.003
        RANGE_UP = 0.005
        BINS = 50
    return BINS, RANGE_LOW, RANGE_UP
