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
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
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
        SIGMA_UP = 0.002
    elif int(ecms == 4230):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4237):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4245):
        MEAN_LOW = -0.0015
        MEAN_UP = 0.001
        SIGMA_UP = 0.0012
    elif int(ecms == 4246):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4260):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.008
    elif int(ecms == 4270):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
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
        MEAN_UP = 0.004
        SIGMA_UP = 0.003
    elif int(ecms == 4360):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4380):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4390):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4400):
        MEAN_LOW = -0.003
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4420):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4440):
        MEAN_LOW = -0.002
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
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.004
    elif int(ecms == 4600):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4610):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4620):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.006
    elif int(ecms == 4640):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4660):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4680):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4700):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4740):
        MEAN_LOW = -0.002
        MEAN_UP = 0.002
        SIGMA_UP = 0.006
    elif int(ecms == 4750):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4780):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4840):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    elif int(ecms == 4914):
        MEAN_LOW = -0.002
        MEAN_UP = 0.003
        SIGMA_UP = 0.004
    elif int(ecms == 4946):
        MEAN_LOW = -0.003
        MEAN_UP = 0.003
        SIGMA_UP = 0.003
    return MEAN_LOW, MEAN_UP, SIGMA_UP

def param_max(ecms):
    MAX = 999
    if int(ecms) == 4340:
        MAX = 30
    if int(ecms) == 4360:
        MAX = 50
    if int(ecms) == 4380:
        MAX = 70
    if int(ecms) == 4390:
        MAX = 20
    if int(ecms) == 4400:
        MAX = 70
    if int(ecms) == 4420:
        MAX = 150
    if int(ecms) == 4440:
        MAX = 80
    if int(ecms) == 4470:
        MAX = 20
    if int(ecms) == 4530:
        MAX = 20
    if int(ecms) == 4575:
        MAX = 15
    if int(ecms) == 4600:
        MAX = 70
    if int(ecms) == 4610:
        MAX = 20
    if int(ecms) == 4620:
        MAX = 45
    if int(ecms) == 4640:
        MAX = 40
    if int(ecms) == 4660:
        MAX = 35
    if int(ecms) == 4680:
        MAX = 90
    if int(ecms) == 4700:
        MAX = 30
    if int(ecms) == 4740:
        MAX = 20.
    if int(ecms) == 4750:
        MAX = 30.
    if int(ecms) == 4780:
        MAX = 40.
    if int(ecms) == 4840:
        MAX = 40.
    if int(ecms) == 4914:
        MAX = 20.
    if int(ecms) == 4946:
        MAX = 15.
    return MAX
