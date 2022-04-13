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
    MEAN_LOW = 999.
    MEAN_UP = 999.
    SIGMA_UP = 999.
    if int(ecms == 4190):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.002
        SIGMA_UP = 0.001
    elif int(ecms == 4200):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.0012
    elif int(ecms == 4210):
        MEAN_LOW = -0.001
        MEAN_UP = 0.001
        SIGMA_UP = 0.002
    elif int(ecms == 4220):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4230):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4237):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.002
    elif int(ecms == 4245):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.0012
    elif int(ecms == 4246):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4260):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4270):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4280):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.001
    elif int(ecms == 4290):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.01
    elif int(ecms == 4310):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.002
    elif int(ecms == 4315):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4340):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.01
    elif int(ecms == 4360):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4380):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4390):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4400):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4420):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4440):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4470):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4530):
        MEAN_LOW = -0.002
        MEAN_UP = 0.005
        SIGMA_UP = 0.006
    elif int(ecms == 4575):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4600):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4610):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4620):
        MEAN_LOW = -0.003
        MEAN_UP = 0.005
        SIGMA_UP = 0.004
    elif int(ecms == 4640):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4660):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4680):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4700):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4840):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    return MEAN_LOW, MEAN_UP, SIGMA_UP
