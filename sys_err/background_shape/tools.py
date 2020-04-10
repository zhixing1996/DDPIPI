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

# parameter of rm(Dpipi) fit
def param_rm_Dpipi(ecms):
    MEAN_UP = 999.
    MEAN_LOW = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        MEAN_UP = 1.872
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    if int(ecms == 4200):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    if int(ecms == 4210):
        MEAN_UP = 1.873
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    if int(ecms == 4220):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    if int(ecms == 4230):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    if int(ecms == 4237):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    if int(ecms == 4245):
        MEAN_UP = 1.873
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    if int(ecms == 4246):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    if int(ecms == 4260):
        MEAN_UP = 1.875
        MEAN_LOW = 1.865
        SIGMA_UP = 0.01
    if int(ecms == 4270):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    if int(ecms == 4280):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4290):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4310):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4315):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4340):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.012
    elif int(ecms == 4360):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4380):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4390):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4400):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4420):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4440):
        MEAN_UP = 1.875
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4470):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.008
    elif int(ecms == 4530):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4575):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    elif int(ecms == 4600):
        MEAN_UP = 1.872
        MEAN_LOW = 1.867
        SIGMA_UP = 0.01
    return MEAN_UP, MEAN_LOW, SIGMA_UP

# luminosity
def luminosity(ecms):
    if int(ecms) == 4190:
        LUM = 526.7 + 43.33
    if int(ecms) == 4200:
        LUM = 526.0
    if int(ecms) == 4210:
        LUM = 517.1 + 54.95
    if int(ecms) == 4220:
        LUM = 514.6 + 54.60
    if int(ecms) == 4230:
        LUM = 44.54 + 1056.4
    if int(ecms) == 4237:
        LUM = 530.3
    if int(ecms) == 4245:
        LUM = 55.88
    if int(ecms) == 4246:
        LUM = 538.1
    if int(ecms) == 4260:
        LUM = 828.4
    if int(ecms) == 4270:
        LUM = 531.1
    if int(ecms) == 4280:
        LUM = 175.7
    if int(ecms) == 4290:
        LUM = 500.
    if int(ecms) == 4310:
        LUM = 45.08
    if int(ecms) == 4315:
        LUM = 500.
    if int(ecms) == 4340:
        LUM = 500.
    if int(ecms) == 4360:
        LUM = 543.9
    if int(ecms) == 4380:
        LUM = 500.
    if int(ecms) == 4390:
        LUM = 55.57
    if int(ecms) == 4400:
        LUM = 500.
    if int(ecms) == 4420:
        LUM = 46.8 + 1043.9
    if int(ecms) == 4440:
        LUM = 570.
    if int(ecms) == 4470:
        LUM = 111.09
    if int(ecms) == 4530:
        LUM = 112.12
    if int(ecms) == 4575:
        LUM = 48.93
    if int(ecms) == 4600:
        LUM = 586.9
    return LUM
